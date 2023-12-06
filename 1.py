my_dict = {
    'list1': [('apple', 5), ('banana', 2), ('orange', 8), ('grape', 3)],
    'list2': [('cat', 10), ('dog', 7), ('bird', 2), ('fish', 5)]
}

# Sort each list based on the values
for key, value_list in my_dict.items():
    my_dict[key] = sorted(value_list, key=lambda x: x[1])

# Print the sorted dictionary
for key, value_list in my_dict.items():
    print(f"{key}: {value_list}")
