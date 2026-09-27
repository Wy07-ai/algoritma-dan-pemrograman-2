"""
tests/test_storage_persistence.py
------------------------------------
Uji integritas simpan-baca data pada penyimpanan lokal (LocalDB + Repository),
termasuk skenario create, read, update, delete, dan cache read-through pada
DataService.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import shutil
import tempfile
import unittest


class TestStoragePersistence(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())

        from config.database_config import DatabaseConfig
        from src.storage.local_db import LocalDB
        from src.storage.repository import Repository
        from src.storage.cache_store import CacheStore

        self.config = DatabaseConfig(db_path=self.tmp_dir / "test.db")
        self.db = LocalDB(self.config)
        self.db.connect()
        self.db.migrate()

        self.repo = Repository(self.db)
        self.cache = CacheStore(max_items=10)

    def tearDown(self):
        self.db.close()
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_insert_and_read_back(self):
        entity_id = self.repo.add("item", {"name": "Test Item", "description": "abc"})
        item = self.repo.get("item", entity_id)

        self.assertIsNotNone(item)
        self.assertEqual(item["name"], "Test Item")

    def test_update_and_delete(self):
        entity_id = self.repo.add("item", {"name": "Old Name", "description": ""})
        ok_update = self.repo.update("item", entity_id, {"name": "New Name", "description": ""})
        updated = self.repo.get("item", entity_id)

        self.assertTrue(ok_update)
        self.assertEqual(updated["name"], "New Name")

        ok_delete = self.repo.delete("item", entity_id)
        self.assertTrue(ok_delete)
        self.assertIsNone(self.repo.get("item", entity_id))

    def test_data_service_cache_read_through(self):
        from src.services.data_service import DataService

        service = DataService(self.repo, self.cache)
        item = service.create_item("Cached Item", "desc")

        # Panggilan pertama: masuk cache. Panggilan kedua: harus dari cache.
        fetched_1 = service.get_item(item["id"])
        fetched_2 = service.get_item(item["id"])

        self.assertEqual(fetched_1, fetched_2)
        self.assertIn(f"item:{item['id']}", self.cache)

    def test_persistence_survives_reconnect(self):
        from src.storage.local_db import LocalDB

        entity_id = self.repo.add("item", {"name": "Persisted", "description": ""})
        self.db.commit()
        self.db.close()

        # Buka koneksi baru ke berkas SQLite yang sama.
        new_db = LocalDB(self.config)
        new_db.connect()
        item = new_db.find_by_id("item", entity_id)

        self.assertIsNotNone(item)
        self.assertEqual(item["name"], "Persisted")
        new_db.close()


if __name__ == "__main__":
    unittest.main()
