import random, sys, time

# Hash function.
#
# |key|: string
# Return value: a hash value
def calculate_hash(key):
    assert type(key) == str
    # Note: This is not a good hash function. Do you see why?
    # Answer: Anagram will have the same hash value because the hash function is summing up the Unicode values of the characters.
    # ex. ABA and BAA will have the same hash value
    hash = 0
    for i, ch in enumerate(key):
        hash += ord(ch) * (128**i)
        # ord関数とはPythonで文字をUnicode値に変換する関数
    return hash

class Item:
    def __init__(self, key, value, next):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next

class HashTable:
    def __init__(self):
        self.bucket_size = 97
        self.buckets = [None] * self.bucket_size
        self.item_count = 0

    def put(self, key, value):
        assert type(key) == str
        self.check_size()
        self.check_usage()
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                item.value = value
                return False
            item = item.next
        new_item = Item(key, value, self.buckets[bucket_index])
        self.buckets[bucket_index] = new_item
        self.item_count += 1
        return True

    def get(self, key):
        assert type(key) == str
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                return (item.value, True)
            item = item.next
        return (None, False)

    def delete(self, key):
        assert type(key) == str
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        prev = None
        while item:
            if item.key == key:
                if prev:
                    prev.next = item.next
                else:
                    self.buckets[bucket_index] = item.next
                self.item_count -= 1
                return True
            prev = item
            item = item.next
        # 縮小処理したい
        # 30%以下になったら縮小する
        # checkする関数を呼ぶ
        return False

    def size(self):
        return self.item_count

    def check_size(self):
        assert (self.bucket_size < 100 or
                self.item_count >= self.bucket_size * 0.3)

    def check_usage(self):
        if self.item_count >= self.bucket_size * 0.7:
            self.resize()

    def resize(self):
        new_size = self.bucket_size * 2
        new_buckets = [None] * new_size
        for bucket in self.buckets:
            item = bucket
            while item:
                bucket_index = calculate_hash(item.key) % new_size
                new_item = Item(item.key, item.value, new_buckets[bucket_index])
                new_buckets[bucket_index] = new_item
                item = item.next
        self.bucket_size = new_size
        self.buckets = new_buckets


# Test the functional behavior of the hash table.
def functional_test():
    hash_table = HashTable()

    assert hash_table.put("aaa", 1) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.size() == 1

    assert hash_table.put("bbb", 2) == True
    assert hash_table.put("ccc", 3) == True
    assert hash_table.put("ddd", 4) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.get("bbb") == (2, True)
    assert hash_table.get("ccc") == (3, True)
    assert hash_table.get("ddd") == (4, True)
    assert hash_table.get("a") == (None, False)
    assert hash_table.get("aa") == (None, False)
    assert hash_table.get("aaaa") == (None, False)
    assert hash_table.size() == 4

    assert hash_table.put("aaa", 11) == False
    assert hash_table.get("aaa") == (11, True)
    assert hash_table.size() == 4

    assert hash_table.delete("aaa") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.size() == 3

    assert hash_table.delete("a") == False
    assert hash_table.delete("aa") == False
    assert hash_table.delete("aaa") == False
    assert hash_table.delete("aaaa") == False

    assert hash_table.delete("ddd") == True
    assert hash_table.delete("ccc") == True
    assert hash_table.delete("bbb") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.get("bbb") == (None, False)
    assert hash_table.get("ccc") == (None, False)
    assert hash_table.get("ddd") == (None, False)
    assert hash_table.size() == 0

    assert hash_table.put("abc", 1) == True
    assert hash_table.put("acb", 2) == True
    assert hash_table.put("bac", 3) == True
    assert hash_table.put("bca", 4) == True
    assert hash_table.put("cab", 5) == True
    assert hash_table.put("cba", 6) == True
    assert hash_table.get("abc") == (1, True)
    assert hash_table.get("acb") == (2, True)
    assert hash_table.get("bac") == (3, True)
    assert hash_table.get("bca") == (4, True)
    assert hash_table.get("cab") == (5, True)
    assert hash_table.get("cba") == (6, True)
    assert hash_table.size() == 6

    assert hash_table.delete("abc") == True
    assert hash_table.delete("cba") == True
    assert hash_table.delete("bac") == True
    assert hash_table.delete("bca") == True
    assert hash_table.delete("acb") == True
    assert hash_table.delete("cab") == True
    assert hash_table.size() == 0
    print("Functional tests passed!")


# Test the performance of the hash table.
#
# Your goal is to make the hash table work with mostly O(1).
# If the hash table works with mostly O(1), the execution time of each iteration
# should not depend on the number of items in the hash table. To achieve the
# goal, you will need to 1) implement rehashing (Hint: expand / shrink the hash
# table when the number of items in the hash table hits some threshold) and
# 2) tweak the hash function (Hint: think about ways to reduce hash conflicts).
def performance_test():
    hash_table = HashTable()

    for iteration in range(100):
        begin = time.time()
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.put(str(rand), str(rand))
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.get(str(rand))
        end = time.time()
        print("%d %.6f" % (iteration, end - begin))

    for iteration in range(100):
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.delete(str(rand))

    assert hash_table.size() == 0
    print("Performance tests passed!")


if __name__ == "__main__":
    functional_test()
    performance_test()