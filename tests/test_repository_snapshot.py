"""Validate the staged project snapshot before its initial upload."""
import subprocess
import unittest


class RepositorySnapshotTests(unittest.TestCase):
    def test_source_and_demo_are_included(self):
        files = subprocess.check_output(
            ["git", "ls-files"], text=True
        ).splitlines()
        for path in ("AGENTS.md", "laya/README.md", "laya/pyproject.toml",
                     "demo/make_tickets.py", "demo/tickets.csv"):
            self.assertIn(path, files)
        self.assertFalse(any(p.startswith(".workbuddy/") for p in files))
        self.assertFalse(any(p.startswith("demo/tickets-checkpoint/") for p in files))

    def test_source_is_not_a_gitlink(self):
        entries = subprocess.check_output(
            ["git", "ls-files", "--stage"], text=True
        ).splitlines()
        self.assertFalse(any(line.startswith("160000 ") for line in entries))

    def test_generated_and_sensitive_paths_are_ignored(self):
        for path in (".env", "credentials.json", ".workbuddy/memory/note.md",
                     "demo/tickets-checkpoint/model.safetensors",
                     "demo/__pycache__/example.pyc"):
            result = subprocess.run(["git", "check-ignore", "-q", path])
            self.assertEqual(result.returncode, 0, path)


if __name__ == "__main__":
    unittest.main()
