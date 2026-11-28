import json
import pathlib
import subprocess
import sys
import unittest

HOOK = pathlib.Path(__file__).resolve().parents[1] / "hooks/codex-forced-rm.py"


def run(command):
    event = {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": command}}
    return subprocess.run([sys.executable, str(HOOK)], input=json.dumps(event),
                          capture_output=True, text=True).returncode


class ForcedRm(unittest.TestCase):
    def test_blocks_forced_rm(self):
        for command in [
            "rm -rf /tmp/x",
            "rm -f results/a*.mp4 results/b*.log",
            "/bin/rm -fr x",
            "rm -r -f x",
            "rm --force x",
            "rm x -f",
            "sudo rm -rf x",
            "env A=1 rm -rf x",
            "cd /tmp && rm -rf x",
            "ls\nrm -f x",
            "if [ -d x ]; then rm -rf x; fi",
            "for f in a b; do rm -f \"$f\"; done",
            "bash -lc 'rm -rf x'",
            # The command from the stalled render thread: heredoc with unbalanced quotes, then rm -f.
            "python3 - <<'PY'\ns=s.replace('out=\\\"x\\\"','tag=${TAG:-}')\nPY\nrm -f results/source-t0-s*.mp4\n",
        ]:
            with self.subTest(command=command):
                self.assertEqual(run(command), 2)

    def test_allows_everything_else(self):
        for command in [
            "rm x",
            "rm -r x",
            "rm -- -f",
            "find /tmp/x -delete",
            "find results -maxdepth 1 -name 'a*' -delete",
            "git rm -f x",
            "echo 'rm -rf x'",
            "grep -rn 'rm -rf' .",
            "ls -lf",
            "",
        ]:
            with self.subTest(command=command):
                self.assertEqual(run(command), 0)

    def test_malformed_event_passes(self):
        r = subprocess.run([sys.executable, str(HOOK)], input="not json", capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
