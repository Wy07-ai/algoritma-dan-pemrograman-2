"""
tests/test_signal_interruption.py
-------------------------------------
Uji penanganan interupsi sinyal Ctrl+C (SIGINT) agar berkas data tidak
terkorupsi: memastikan callback on_shutdown terpanggil tepat satu kali
lewat jalur SignalHandler, dan pemanggilan sinyal kedua tidak mengulang
proses shutdown (mencegah state ganda / write ganda).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import unittest
from unittest.mock import MagicMock

from src.system.signal_handler import SignalHandler


class TestSignalInterruption(unittest.TestCase):
    def test_first_signal_triggers_shutdown_once(self):
        on_shutdown = MagicMock()
        handler = SignalHandler(on_shutdown=on_shutdown)

        with self.assertRaises(SystemExit) as ctx:
            handler._handle(signum=2, frame=None)  # 2 == SIGINT

        on_shutdown.assert_called_once()
        self.assertEqual(ctx.exception.code, 0)

    def test_second_signal_forces_exit_without_calling_shutdown_again(self):
        on_shutdown = MagicMock()
        handler = SignalHandler(on_shutdown=on_shutdown)

        with self.assertRaises(SystemExit):
            handler._handle(signum=2, frame=None)

        with self.assertRaises(SystemExit) as ctx:
            handler._handle(signum=2, frame=None)

        # on_shutdown tetap hanya terpanggil sekali (dari sinyal pertama).
        on_shutdown.assert_called_once()
        self.assertEqual(ctx.exception.code, 1)

    def test_install_registers_without_error(self):
        handler = SignalHandler(on_shutdown=lambda: None)
        # Harus berjalan tanpa exception di platform manapun.
        handler.install()


if __name__ == "__main__":
    unittest.main()
