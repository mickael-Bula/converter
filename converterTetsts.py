import os
import unittest


class TestConverter(unittest.TestCase):

    def test_directory_not_empty(self):
        path = 'C:/Users/bulam/Documents/modeles'
        self.assertIsNotNone(path, "Le répertoire ne devrait pas être vide")

    def test_count_files(self):
        path = 'C:/Users/bulam/Documents/modeles'
        self.assertEqual(len(os.listdir(path)), 3, "Les fichiers devraient être au nombre de 3")


if __name__ == '__main__':
    unittest.main()
