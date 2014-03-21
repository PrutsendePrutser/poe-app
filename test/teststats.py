import unittest
import sys
import os
sys.path.append('..' + os.sep)
import stats

class testStats(unittest.TestCase):
    
    def setUp(self):
        self.items = stats.items()
        
    # importItems should return a dictionary
    def testImportItems(self):
        self.assertIsInstance(self.items.importItems(), dict)

if __name__ == "__main__":
    unittest.main()