import tempfile
import unittest
from pathlib import Path
import logging

from logger import FileLogger


class FileLoggerTests(unittest.TestCase):
    def setUp(self):
        self.shared_logger = logging.getLogger("document_parser")
        self.original_handlers= self.shared_logger.handlers[:]
        self.original_level = self.shared_logger.level
        self.original_propagate = self.shared_logger.propagate

        for handler in self.shared_logger.handlers:
            self.shared_logger.removeHandler(handler)

        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

    def tearDown(self):
        for handler in self.shared_logger.handlers:
            self.shared_logger.removeHandler(handler)
            handler.close()

        for handler in self.original_handlers:
            self.shared_logger.addHandler(handler)

        self.shared_logger.setLevel(self.original_level)
        self.shared_logger.propagate = self.original_propagate

    def test_two_instances_write_to_same_file(self):
        first_path = Path(self.temp_dir.name) / "first.log"
        second_path = Path(self.temp_dir.name) / "second.log"

        first_logger = FileLogger(str(first_path))
        second_logger = FileLogger(str(second_path))

        first_logger.warning("first_file.txt", 1)
        second_logger.warning(document_filename="second_file.txt", line_number=2)

        for handlers in self.shared_logger.handlers:
            handlers.flush()

        self.assertIn("first_file.txt", first_path.read_text(encoding="utf-8"))
        self.assertIn("second_file.txt", first_path.read_text(encoding="utf-8"))
        self.assertFalse(second_path.exists())


if __name__ == "__main__":
    unittest.main()