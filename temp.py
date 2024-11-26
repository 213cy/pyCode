import time

dict1 = {'a': 1, 'b': 2}
dict2 = {'a': 1, 'b': 3}
dict3 = {'a': 1, 'c': 2}

print(dict1.items() < dict2.items())  # True
print(dict1.items() < dict3.items())  # True
print(dict2.items() < dict3.items())  # False

time.sleep(5)
