class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.base_address = 0
        self.table = [self._create_empty_entry() for _ in range(self.size)]
        
    def _create_empty_entry(self):
        
        return {
            'ID': None,        
            'V': None,         
            'h(V)': None,      
            'B': self.base_address,
            'H': self.size,
            'C': False,        
            'U': False,       
            'T': True,        
            'L': False,       
            'D': False,       
            'P0': None,       
            'Pi': None        
        }
    
    def _hash(self, key):
        
        if isinstance(key, str):
            numeric_value = sum(ord(c) for c in key)
        else:
            numeric_value = hash(key)
        return numeric_value % self.size
    
    def _probe(self, index, attempt):
    
        return (index + attempt**2) % self.size
    
    def _find_entry(self, key):
       
        hash_index = self._hash(key)
        prev_index = None
        
        for attempt in range(self.size):
            current_index = self._probe(hash_index, attempt)
            entry = self.table[current_index]
            
           
            if entry['U'] and not entry['D'] and entry['ID'] == key:
                return entry, current_index, prev_index
           
            if entry['U'] and not entry['D']:
                prev_index = current_index
            
            if entry['T'] and not entry['L']:
                break
                
        return None, None, None
    
    def _find_insert_position(self, key):
        
        hash_index = self._hash(key)
        
        for attempt in range(self.size):
            current_index = self._probe(hash_index, attempt)
            entry = self.table[current_index]
            
            
            if not entry['U'] or entry['D']:
                return current_index
                
            
            if entry['ID'] == key and not entry['D']:
                return current_index
                
        
        self._resize()
        return self._find_insert_position(key)  
    
    def insert(self, key, value):
       
        numeric_value = sum(ord(c) for c in key) if isinstance(key, str) else hash(key)
        entry, existing_index, _ = self._find_entry(key)
        
        
        if entry is not None:
            self.table[existing_index]['Pi'] = value
            self.table[existing_index]['V'] = numeric_value
            return
        
        
        insert_index = self._find_insert_position(key)
        new_entry = self.table[insert_index]
        
       
        new_entry.update({
            'ID': key,
            'V': numeric_value,
            'h(V)': self._hash(key),
            'U': True,
            'D': False,
            'Pi': value,
            'T': True
        })
        
        
        if insert_index != self._hash(key):
            
            hash_index = self._hash(key)
            last_index = hash_index
            while self.table[last_index]['L'] and self.table[last_index]['P0'] is not None:
                last_index = self.table[last_index]['P0']
            
            self.table[last_index]['P0'] = insert_index
            self.table[last_index]['L'] = True
            self.table[last_index]['T'] = False
            new_entry['C'] = True
    
    def get(self, key):
      
        entry, _, _ = self._find_entry(key)
        return entry['Pi'] if entry else None
    
    def delete(self, key):
     
        entry, current_index, prev_index = self._find_entry(key)
        if entry is None:
            return
       
        self.table[current_index]['U'] = False
        self.table[current_index]['D'] = True
       
        if self.table[current_index]['L']:
            next_index = self.table[current_index]['P0']
           
            self.table[current_index].update({
                'ID': self.table[next_index]['ID'],
                'V': self.table[next_index]['V'],
                'h(V)': self.table[next_index]['h(V)'],
                'Pi': self.table[next_index]['Pi'],
                'U': True,
                'D': False,
                'P0': self.table[next_index]['P0'],
                'L': self.table[next_index]['L'],
                'T': self.table[next_index]['T']
            })
            
            self.table[next_index].update(self._create_empty_entry())
        elif prev_index is not None:
            
            self.table[prev_index]['P0'] = None
            self.table[prev_index]['L'] = False
            self.table[prev_index]['T'] = True
    
    def _resize(self):
        
        old_table = self.table
        self.size *= 2
        self.table = [self._create_empty_entry() for _ in range(self.size)]
      
        for entry in old_table:
            if entry['U'] and not entry['D']:
                self.insert(entry['ID'], entry['Pi'])
    
    def display_table(self):
        
        print(f"{'Index':<6} | {'ID':<15} | {'h(V)':<5} | {'C':<2} | {'U':<2} | "
              f"{'T':<2} | {'L':<2} | {'D':<2} | {'P0':<5} | {'Pi':<10}")
        print("-" * 80)
        for i, entry in enumerate(self.table):
            print(f"{i:<6} | {str(entry['ID']):<15} | {str(entry['h(V)']):<5} | "
                  f"{int(entry['C']):<2} | {int(entry['U']):<2} | {int(entry['T']):<2} | "
                  f"{int(entry['L']):<2} | {int(entry['D']):<2} | "
                  f"{str(entry['P0']):<5} | {str(entry['Pi']):<10}")



if __name__ == "__main__":
    ht = HashTable(size=5)
    
    print("Пустая таблица:")
    ht.display_table()
    print("\n")
    
    
    ht.insert("apple", 10)
    ht.insert("banana", 20)
    ht.insert("orange", 30)
    ht.insert("apple", 15)  
    
    print("Таблица после вставки:")
    ht.display_table()
    print("\n")
    
    print("Значение для 'apple':", ht.get("apple"))
    print("Значение для 'banana':", ht.get("banana"))
    print("Значение для 'grape':", ht.get("grape"))  
    print("\n")
    
    
    ht.delete("banana")
    print("Таблица после удаления 'banana':")
    ht.display_table()
    print("\n")
    
    
    print("Значение для 'banana' после удаления:", ht.get("banana"))
    print("\n")
    

    ht.insert("lemon", 40)
    ht.insert("melon", 50)
    ht.insert("mleon", 50)
    ht.insert("pear", 60)  
    
    print("Таблица после добавления новых элементов и ресайза:")
    ht.display_table()