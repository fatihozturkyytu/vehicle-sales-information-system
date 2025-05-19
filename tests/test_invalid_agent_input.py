import unittest
from unittest.mock import patch
import sqlite3
from manager_gui import add_agent, DB_PATH
import os

DB_PATH = "test_users.db"


class TestInvalidAgentInput(unittest.TestCase):

    def setUp(self):
        add_agent.DB_PATH = DB_PATH
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    @patch('manager_gui.simpledialog.askstring')
    @patch('manager_gui.messagebox.showerror')
    @patch('manager_gui.messagebox.showinfo')
    def test_add_agent_with_empty_input(self, mock_info, mock_error, mock_askstring):
        # İlk çağrıda ID boş, ikinci çağrıda şifre boş olacak
        mock_askstring.side_effect = ["", "123456"]
        add_agent()
        mock_error.assert_called_with("Hata", "Boş alan bırakmayın.")

        mock_askstring.side_effect = ["valid_id", ""]
        add_agent()
        self.assertEqual(mock_error.call_count, 2)

        # Veritabanına eklenmediğini doğrulama
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id = 'valid_id'")
        result = c.fetchone()
        conn.close()
        self.assertIsNone(result)

   # @classmethod
    #def tearDownClass(cls):
        # Test sonunda veritabanını sil
     #   if os.path.exists(DB_PATH):
      #      os.remove(DB_PATH)

if __name__ == '__main__':
    unittest.main()
