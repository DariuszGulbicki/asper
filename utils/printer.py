def trim_string(string, length):
    if len(string) > length:
        return string[:length - 3] + "..."
    return string

def trim_table(table, length):
    for row in table:
        for i in range(len(row)):
            if row[i] != None:
                row[i] = trim_string(row[i], length)
    return table

def remove_none_rows(table):
    return list(filter(lambda row: not all(item == None for item in row), table))

# Trim all text in list to specified length
# if exceeded replace last 3 characters of the trimmed text with "..."
def trim_list(list, length):
    return [trim_string(item, length) for item in list]

# Table style:
# +----------+----------+
# | header 1 | header 2 |
# +----------+----------+
# |  cell 1  |  cell 2  |
# +----------+----------+
# Trim all text in cells to specified length (if exceeded replace last 3 characters of the trimmed text with "...")
# Ignore None types in table
# table argument is a list of lists
# If a row is Full of None types, it will be ignored
# print bottom and top borders
# prints joints as "+" by default
def pretty_print_table(table, headers, trim=50, vertical_char="|", horizontal_char="-", joint_char="+"):
    table = trim_table(table, trim)
    table = remove_none_rows(table)
    table.insert(0, headers)
    column_widths = []
    for i in range(len(table[0])):
        column_widths.append(max([len(str(row[i])) for row in table]))
    print(joint_char + joint_char.join([horizontal_char * width for width in column_widths]) + joint_char)
    for row in table:
        print(vertical_char + vertical_char.join([str(cell).ljust(width) for cell, width in zip(row, column_widths)]) + vertical_char)
        print(joint_char + joint_char.join([horizontal_char * width for width in column_widths]) + joint_char)

# List style:
# +----------+----------+----------+
# |  item 1  |  item 2  |  item 3  |
# +----------+----------+----------+
# If list is empty or none ignore it
# print bottom and top borders
# prints joints as "+" by default
# trim all text in cells to specified length (if exceeded replace last 3 characters of the trimmed text with "...")
def pretty_print_list_horizontal(hlist, trim=50, vertical_char="|", horizontal_char="-", joint_char="+"):
    if hlist != None and len(hlist) > 0:
        hlist = trim_list(hlist, trim)
        column_widths = []
        for i in range(len(hlist)):
            column_widths.append(max([len(str(item)) for item in hlist]))
        print(joint_char + joint_char.join([horizontal_char * width for width in column_widths]) + joint_char)
        print(vertical_char + vertical_char.join([str(item).ljust(width) for item, width in zip(hlist, column_widths)]) + vertical_char)
        print(joint_char + joint_char.join([horizontal_char * width for width in column_widths]) + joint_char)

# List style:
# +----------+
# |  item 1  |
# |  item 2  |
# |  item 3  |
# +----------+
# If list is empty or none ignore it
# print bottom and top borders
# prints joints as "+" by default
# trim all text in cells to specified length (if exceeded replace last 3 characters of the trimmed text with "...")
# LIST CONTAINS ONLY ONE COLUMN
def pretty_print_list_vertical(hlist, trim=50, vertical_char="|", horizontal_char="-", joint_char="+"):
    if hlist is None or len(hlist) == 0:
        return
    hlist = [x[:trim] + "..." if len(x) > trim else x for x in hlist]
    max_length = max([len(x) for x in hlist])
    print(joint_char + horizontal_char * (max_length + 2) + joint_char)
    for item in hlist:
        print(vertical_char, item.ljust(max_length), vertical_char)
    print(joint_char + horizontal_char * (max_length + 2) + joint_char)

# Print style:
# +---------------+
# |  key = value  |
# |  key = value  |
# |  key = value  |
# +---------------+
# If dictionary is empty or none ignore it
# print bottom and top borders
# prints joints as "+" by default
# trim all text in cells to specified length (if exceeded replace last 3 characters of the trimmed text with "...")
def pretty_print_dict_vertical(dictionary, trim=50, vertical_char="|", horizontal_char="-", joint_char="+"):
    if dictionary is None or len(dictionary) == 0:
        return
    max_key_length = max([len(str(key)) for key in dictionary.keys()])
    max_value_length = max([len(str(value)) for value in dictionary.values()])
    max_length = max_key_length + max_value_length + 3
    print(joint_char + horizontal_char * (max_length + 2) + joint_char)
    for key, value in dictionary.items():
        print(vertical_char, str(key).ljust(max_key_length), "=", str(value).ljust(max_value_length), vertical_char)
    print(joint_char + horizontal_char * (max_length + 2) + joint_char)

def print_welcome_screen(version):
    print(f"""
                    _____  _____   ______  _____  
            /\\     / ____||  __ \\ |  ____||  __ \\\n 
           /  \\   | (___  | |__) || |__   | |__) |\n
          / /\ \\   \___ \ |  ___/ |  __|  |  _  / \n
         / ____ \\  ____) || |     | |____ | | \ \ \n
        /_/    \_\\|_____/ |_|     |______||_|  \_\\\n  
        \n                                                                                                                             
        \n
        ASPER - Assistant Personalities (Version {version})
    """)