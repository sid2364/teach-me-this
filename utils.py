import os

# Output file where you'll store the names
output_file = 'saved_file_names.txt'
data_dir = 'data'
files_to_read = glob.glob('data/*.pdf')

def create_new_db_or_read_existing():
    # List files and write their names to a file
    with open(output_file, 'r') as file:
        saves_file_names = file.readlines()
        saved_file_names = [name.strip() for name in file_names]

    if set(saved_file_names) == set(files_to_read):
        return read_lancedb()

    #else write a new lancedb since we don't have these new books stored and return that instance (will take longer)

    with open(output_file, 'w') as file:
        for filename in files_to_read:
            file.write(f"{filename}\n")
    return write_new_lancedb()

def read_lancedb():
    pass #todo

def write_new_lancedb():
    pass


'''
todo
write these functions and make the main.py usethem instead'''