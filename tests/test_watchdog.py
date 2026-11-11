import http.server
import json
import os
import pathlib
import socketserver
import subprocess
import tempfile
import threading
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PING = ROOT / "bin/agent-ping"
HEALTH = ROOT / "bin/agent-health"


class Handler(http.server.BaseHTTPRequestHandler):
    requests = []

    def do_POST(self):
        body = self.rfile.read(int(self.headers["Content-Length"]))
        self.__class__.requests.append((dict(self.headers), json.loads(body)))
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, *_):
        pass


class WatchdogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = pathlib.Path(self.tmp.name)
        (self.home / ".agent-config").mkdir()
        (self.home / ".config" / "agent-ping").mkdir(parents=True)
        (self.home / ".agent-config" / "machine").write_text("test\n")
        Handler.requests = []
        self.server = socketserver.TCPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        creds = {"url": f"http://127.0.0.1:{self.server.server_address[1]}/hook", "key": "test-secret"}
        path = self.home / ".config" / "agent-ping" / "grok.json"
        path.write_text(json.dumps(creds))
        path.chmod(0o600)

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.tmp.cleanup()

    def env(self, extra=None):
        env = dict(os.environ, HOME=str(self.home), PYTHONPATH=str(ROOT))
        if extra: env.update(extra)
        return env

    def execute(self, script, *args, env=None, **kwargs):
        return subprocess.run(["python3", str(script), *args], env=env or self.env(), text=True,
                              capture_output=True, **kwargs)

    def test_ping_payload_and_dedupe(self):
        first = self.execute(PING, "--from", "health", "--level", "warn", "--key", "test:disk", "Disk is full")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(len(Handler.requests), 1)
        headers, body = Handler.requests[0]
        self.assertEqual(headers["Authorization"], "Bearer test-secret")
        self.assertEqual(body["machine"], "test")
        second = self.execute(PING, "--from", "health", "--level", "warn", "--key", "test:disk", "Disk is full")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(len(Handler.requests), 1)
        self.assertIn("deduped", second.stdout)

    def test_missing_credentials_is_exit_three(self):
        (self.home / ".config" / "agent-ping" / "grok.json").unlink()
        result = self.execute(PING, "--from", "health", "--level", "warn", "Broken")
        self.assertEqual(result.returncode, 3)
        self.assertIn("credentials not found", result.stderr)

    def test_health_requires_two_failures_then_recovers(self):
        marker = self.home / "healthy"
        config = self.home / "check.json"
        config.write_text(json.dumps({"checks": [{"id": "marker", "kind": "command",
            "argv": ["sh", "-lc", f"test -f {marker}"], "needs": "Create the marker."}]}))
        extra = {"AGENT_HEALTH_CONFIG": str(config), "AGENT_HEALTH_STATE_DIR": str(self.home / "state"),
                 "AGENT_HEALTH_PERSIST_MINUTES": "0"}
        first = self.execute(HEALTH, "check", **{"env": self.env(extra)})
        self.assertNotEqual(first.returncode, 0)
        self.assertEqual(len(Handler.requests), 0)
        second = self.execute(HEALTH, "check", **{"env": self.env(extra)})
        self.assertNotEqual(second.returncode, 0)
        self.assertEqual(len(Handler.requests), 1)
        events = [json.loads(line) for line in (self.home / "state" / "events.jsonl").read_text().splitlines()]
        self.assertEqual(events[0]["state"], "warn")
        self.assertFalse(events[0]["pinged"])
        marker.touch()
        recovered = self.execute(HEALTH, "check", **{"env": self.env(extra)})
        self.assertEqual(recovered.returncode, 0, recovered.stderr)
        self.assertEqual(len(Handler.requests), 2)
        self.assertIn("recovered", Handler.requests[-1][1]["message"])

    def test_brief_failure_stays_silent(self):
        marker = self.home / "healthy"
        config = self.home / "check.json"
        config.write_text(json.dumps({"checks": [{"id": "marker", "kind": "command",
            "argv": ["sh", "-lc", f"test -f {marker}"]}]}))
        extra = {"AGENT_HEALTH_CONFIG": str(config), "AGENT_HEALTH_STATE_DIR": str(self.home / "state")}
        for _ in range(3):
            self.execute(HEALTH, "check", **{"env": self.env(extra)})
        marker.touch()
        self.execute(HEALTH, "check", **{"env": self.env(extra)})
        self.assertEqual(len(Handler.requests), 0)

    def test_dry_run_has_no_request(self):
        result = self.execute(PING, "--from", "health", "--level", "info", "--dry-run", "All good")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(Handler.requests), 0)
        self.assertEqual(json.loads(result.stdout)["message"], "All good")


if __name__ == "__main__":
    unittest.main()
