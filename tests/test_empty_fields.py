import unittest
from unittest.mock import patch
import sqlite3
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import manager_gui

TEST_DB = "test_users.db"

class TestEmptyFields(unittest.TestCase):

    def setUp(self):
        # Test veritabanını kullan
        manager_gui.DB_PATH = TEST_DB
        conn = sqlite3.connect(TEST_DB)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id TEXT PRIMARY KEY,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL)''')
        conn.commit()
        conn.close()


    @patch('manager_gui.simpledialog.askstring')
    @patch('manager_gui.messagebox.showerror')
    def test_empty_fields_should_show_error_and_not_insert(self, mock_error, mock_askstring):
        mock_askstring.side_effect = ["", "123"]
        manager_gui.add_agent()

        conn = sqlite3.connect(TEST_DB)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id = ''")
        result = c.fetchone()
        conn.close()

        self.assertIsNone(result)
        mock_error.assert_called_once_with("Hata", "Boş alan bırakmayın.")

if __name__ == "__main__":
    unittest.main()
