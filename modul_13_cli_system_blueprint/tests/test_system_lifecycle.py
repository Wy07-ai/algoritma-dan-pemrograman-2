"""
tests/test_system_lifecycle.py
--------------------------------
Uji proses booting & shutdown sistem: memastikan Kernel.boot() menghasilkan
AppContext yang lengkap, dan Kernel.shutdown() membersihkan context tanpa error.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import shutil
import tempfile
import unittest


class TestSystemLifecycle(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())

        import config.settings as settings_module

        self._original_settings = settings_module.settings
        settings_module.settings = settings_module.Settings(data_dir=self.tmp_dir)

        import config.database_config as db_config_module

        db_config_module.database_config = db_config_module.DatabaseConfig(
            db_path=self.tmp_dir / "test_store.db"
        )

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_boot_creates_full_context(self):
        from src.system.kernel import Kernel

        kernel = Kernel()
        ctx = kernel.boot()

        self.assertIsNotNone(ctx.repository)
        self.assertIsNotNone(ctx.session)
        self.assertIsNotNone(ctx.cache)
        self.assertTrue((self.tmp_dir).exists())

        kernel.shutdown()
        self.assertIsNone(kernel.context)

    def test_shutdown_without_boot_is_safe(self):
        from src.system.kernel import Kernel

        kernel = Kernel()
        # Tidak boot() dulu -> shutdown harus tetap aman, tidak melempar error.
        kernel.shutdown()
        self.assertIsNone(kernel.context)


if __name__ == "__main__":
    unittest.main()
