import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dv_workspace_materializer import materialize_local, run


class WorkspaceMaterializerTests(unittest.TestCase):
    def test_local_plumbing_preserves_blob_bytes_without_checkout_filters(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            destination = root / "destination"
            source.mkdir()
            run(["git", "init", "--quiet"], source)
            run(["git", "config", "user.name", "fixture"], source)
            run(["git", "config", "user.email", "fixture@example.invalid"], source)
            expected = b"line one\nline two\n"
            (source / "tracked.txt").write_bytes(expected)
            run(["git", "add", "tracked.txt"], source)
            run(["git", "commit", "--quiet", "-m", "fixture"], source)
            revision = run(["git", "rev-parse", "HEAD"], source)

            identity = materialize_local(source, revision, destination)

            actual = (destination / "tracked.txt").read_bytes()
            self.assertEqual(actual, expected)
            self.assertEqual(identity["head_revision"], revision)
            self.assertEqual(identity["file_sha256"]["tracked.txt"], hashlib.sha256(expected).hexdigest())
            self.assertEqual(identity["symlink_fallbacks"], [])


if __name__ == "__main__":
    unittest.main()
