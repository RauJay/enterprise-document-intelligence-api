import tempfile
import unittest
from pathlib import Path

from logger import FileLogger


class FileLoggerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

    @staticmethod
    def _close_handlers(logger):
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
            handler.close()

    def test_two_instances_write_to_different_file(self):
        first_path = Path(self.temp_dir.name) / "first.log"
        second_path = Path(self.temp_dir.name) / "second.log"

        first_logger = FileLogger(str(first_path))
        self.addCleanup(self._close_handlers, first_logger.logger)

        second_logger = FileLogger(str(second_path))
        self.addCleanup(self._close_handlers, second_logger.logger)

        first_logger.warning("first_file.txt", 1)
        second_logger.warning(document_filename="second_file.txt", line_number=2)

        self.assertNotIn("second_file.txt", first_path.read_text(encoding="utf-8"))
        self.assertNotIn("first_file.txt",  second_path.read_text(encoding="utf-8"))

        self.assertIn("first_file.txt", first_path.read_text(encoding="utf-8"))
        self.assertIn("second_file.txt", second_path.read_text(encoding="utf-8"))

    def test_two_files_with_same_first_name_write_to_different_file(self):
        first_path = Path(self.temp_dir.name) / "report.v1.log"
        second_path = Path(self.temp_dir.name) / "report.v2.log"

        first_logger = FileLogger(str(first_path))
        self.addCleanup(self._close_handlers, first_logger.logger)

        second_logger = FileLogger(str(second_path))
        self.addCleanup(self._close_handlers, second_logger.logger)

        first_logger.warning("first_file.txt", 1)
        second_logger.warning(document_filename="second_file.txt", line_number=2)
        
        self.assertNotIn("second_file.txt", first_path.read_text(encoding="utf-8"))
        self.assertNotIn("first_file.txt",  second_path.read_text(encoding="utf-8"))
        
        self.assertIn("first_file.txt", first_path.read_text(encoding="utf-8"))
        self.assertIn("second_file.txt", second_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()