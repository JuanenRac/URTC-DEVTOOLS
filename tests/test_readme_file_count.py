"""The README files and the file tree state how many shared files there are: the number the set really has."""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import devtools_set  # noqa: E402


class ReadmeFileCountTests(unittest.TestCase):
    def test_the_tree_of_every_readme_states_the_number_of_shared_files(self):
        real = str(len(devtools_set.shared_files()))
        readmes = sorted(ROOT.glob("README*.md"))
        self.assertEqual(len(readmes), 8)
        for readme in readmes:
            tree = [line for line in readme.read_text(encoding="utf-8").splitlines() if line.startswith("├── files/")]
            self.assertEqual([re.findall(r"\d+", line) for line in tree], [[real]], readme.name)

    def test_the_captions_of_the_structure_picture_state_it_too(self):
        real = str(len(devtools_set.shared_files()))
        text = (ROOT / "docs" / "structure.json").read_text(encoding="utf-8")
        captions = [line for line in json.dumps(json.loads(text), ensure_ascii=False, indent=0).splitlines()
                    if re.search(r"canonical|canón|kanonisch|canonique|canonici|规范文件|正規ファイル", line) and re.search(r"\d", line)]
        self.assertTrue(captions)
        for line in captions:
            self.assertIn(real, re.findall(r"\d+", line), line)


if __name__ == "__main__":
    unittest.main()
