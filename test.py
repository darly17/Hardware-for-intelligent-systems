import unittest
from unittest.mock import patch
from main import HashTable  

class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.ht = HashTable(size=5)
        
    def test_initialization(self):
        self.assertEqual(len(self.ht.table), 5)
        for entry in self.ht.table:
            self.assertIsNone(entry['ID'])
            self.assertFalse(entry['U'])
            self.assertEqual(entry['H'], 5)
            
    def test_hash_function_string(self):
        key = "test"
        expected_numeric = sum(ord(c) for c in key)
        expected_hash = expected_numeric % 5
        self.assertEqual(self.ht._hash(key), expected_hash)
        
    def test_hash_function_non_string(self):
        key = 12345
        expected_hash = hash(key) % 5
        self.assertEqual(self.ht._hash(key), expected_hash)
        
    def test_probe_function(self):
       
        self.assertEqual(self.ht._probe(0, 1), 1)   
        self.assertEqual(self.ht._probe(0, 2), 4)   
        self.assertEqual(self.ht._probe(0, 3), 4)  
        
    def test_insert_no_collision(self):
        self.ht.insert("apple", 10)
        found = False
        for entry in self.ht.table:
            if entry['ID'] == "apple":
                found = True
                self.assertEqual(entry['V'], sum(ord(c) for c in "apple"))
                self.assertEqual(entry['Pi'], 10)
                self.assertTrue(entry['U'])
                self.assertFalse(entry['D'])
                self.assertTrue(entry['T'])
                self.assertFalse(entry['C'])
        self.assertTrue(found)
        
    def test_insert_with_collision(self):
     
        with patch.object(self.ht, '_hash', return_value=0):
            self.ht.insert("apple", 10)
            self.ht.insert("banana", 20)
            
            self.assertEqual(self.ht.table[0]['ID'], "apple")
            self.assertFalse(self.ht.table[0]['C'])
            self.assertEqual(self.ht.table[0]['P0'], 1)  
            self.assertTrue(self.ht.table[0]['L'])
            
       
            self.assertEqual(self.ht.table[1]['ID'], "banana")
            self.assertTrue(self.ht.table[1]['C'])
            
    def test_insert_update_existing(self):
        self.ht.insert("apple", 10)
        self.ht.insert("apple", 15)
        
        count = 0
        for entry in self.ht.table:
            if entry['ID'] == "apple":
                count += 1
                self.assertEqual(entry['Pi'], 15)
        self.assertEqual(count, 1)
        
    def test_get_existing(self):
        self.ht.insert("apple", 10)
        self.assertEqual(self.ht.get("apple"), 10)
        
    def test_get_non_existing(self):
        self.assertIsNone(self.ht.get("nonexistent"))
        
    def test_get_after_collision(self):
        with patch.object(self.ht, '_hash', return_value=0):
            self.ht.insert("apple", 10)
            self.ht.insert("banana", 20)
            self.assertEqual(self.ht.get("banana"), 20)
            
    def test_delete_existing(self):
        self.ht.insert("apple", 10)
        self.ht.delete("apple")
        
        for entry in self.ht.table:
            if entry['ID'] == "apple":
                self.assertTrue(entry['D'])
                self.assertFalse(entry['U'])
                
    def test_delete_non_existing(self):
        try:
            self.ht.delete("nonexistent")
        except Exception as e:
            self.fail(f"Delete non-existing raised exception: {e}")
            
    def test_resize(self):
        
        self.ht.insert("apple", 10)
        self.ht.insert("banana", 20)
        self.ht.insert("orange", 30)
        self.ht.insert("lemon", 40)
        self.ht.insert("melon", 50)
        
        self.ht.insert("pear", 60)
        
        self.assertEqual(self.ht.size, 10)
        self.assertEqual(len(self.ht.table), 10)
        
        self.assertEqual(self.ht.get("apple"), 10)
        self.assertEqual(self.ht.get("banana"), None)
        self.assertEqual(self.ht.get("pear"), 60)
        
    
        
    def test_display_table(self):
        
        try:
            self.ht.display_table()
        except Exception as e:
            self.fail(f"display_table raised exception: {e}")
            
        self.ht.insert("apple", 10)
        try:
            self.ht.display_table()
        except Exception as e:
            self.fail(f"display_table with data raised exception: {e}")
        
    def test_insert_multiple_collisions(self):
        
        with patch.object(self.ht, '_hash', return_value=0):
          
            self.ht.insert("apple", 10)
            self.ht.insert("banana", 20)
            self.ht.insert("orange", 30)
            
          
            self.assertEqual(self.ht.table[0]['ID'], "apple")
            self.assertEqual(self.ht.table[0]['P0'], 1)  
            
            self.assertEqual(self.ht.table[1]['ID'], "banana")
            self.assertEqual(self.ht.table[1]['P0'], 4)  
            
            self.assertEqual(self.ht.table[4]['ID'], "orange")

    def test_delete_with_collision_chain(self):
       
        with patch.object(self.ht, '_hash', return_value=0):
            self.ht.insert("apple", 10)
            self.ht.insert("banana", 20)
            self.ht.insert("orange", 30)
            
            
            self.ht.delete("banana")
            
           
            self.assertTrue(self.ht.table[0]['L'])  
            self.assertEqual(self.ht.table[0]['P0'], 1)  
            
            self.assertFalse(self.ht.table[1]['D'])
            self.assertTrue(self.ht.table[1]['U'])
           
            self.assertEqual(self.ht.get("orange"), 30)

    def test_reuse_deleted_slot(self):
       
        self.ht.insert("apple", 10)
        hash_idx = self.ht._hash("apple")
        
        self.ht.delete("apple")
        
      
        self.assertTrue(self.ht.table[hash_idx]['D'])
      
        self.ht.insert("apple", 20)
       
        self.assertEqual(self.ht.table[hash_idx]['ID'], "apple")
        self.assertFalse(self.ht.table[hash_idx]['D'])

    def test_collision_after_deletion(self):
        with patch.object(self.ht, '_hash', return_value=0):
            self.ht.insert("apple", 10)
            self.ht.delete("apple")
            
            self.ht.insert("banana", 20)
            
            self.assertFalse(self.ht.table[0]['C'])
           
            self.ht.insert("orange", 30)
            self.assertFalse(self.ht.table[0]['C'])

    def test_terminal_flag(self):
        
        with patch.object(self.ht, '_hash', return_value=0):
            self.ht.insert("apple", 10)
            self.assertTrue(self.ht.table[0]['T'])  
            
            self.ht.insert("banana", 20)
            self.assertFalse(self.ht.table[0]['T'])  
            self.assertTrue(self.ht.table[1]['T'])  

    def test_link_flag(self):
        
        with patch.object(self.ht, '_hash', return_value=0):
            self.ht.insert("apple", 10)
            self.assertFalse(self.ht.table[0]['L'])  
            
            self.ht.insert("banana", 20)
            self.assertTrue(self.ht.table[0]['L'])   
            self.assertFalse(self.ht.table[1]['L'])  

    def test_edge_case_probing(self):
        
        small_ht = HashTable(size=3)
        
        with patch.object(small_ht, '_hash', return_value=0):
            small_ht.insert("a", 1)
            small_ht.insert("b", 2)
            small_ht.insert("c", 3)  
            
            self.assertEqual(small_ht.size, 6)  

    def test_insert_after_resize(self):
        
        for i in range(5):
            self.ht.insert(f"key{i}", i)
   
        self.ht.insert("new_key", 100)
        
        for i in range(5):
            self.assertEqual(self.ht.get(f"key{i}"), i)
        
        
        self.assertEqual(self.ht.get("new_key"), 100)

   

    def test_negative_numeric_value(self):
        
        self.ht.insert("test", -100)
        for entry in self.ht.table:
            if entry['ID'] == "test":
                self.assertEqual(entry['V'], sum(ord(c) for c in "test"))
                self.assertEqual(entry['Pi'], -100)

    def test_special_characters_key(self):
        
        special_key = "!@#$%^&*()"
        self.ht.insert(special_key, 42)
        self.assertEqual(self.ht.get(special_key), 42)

if __name__ == "__main__":
    unittest.main()