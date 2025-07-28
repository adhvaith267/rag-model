import os

def get_files_in_directory(directory):
    # Get all files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # Create a dictionary with index as key and file name as value
    files_dict = {index: file for index, file in enumerate(files, start=1)}
    
    # Print the dictionary in the desired format
    for index, file_name in files_dict.items():
        print(f"{index} : {file_name}")
    
    # Prompt the user to select a file by entering the number
    user_input = int(input("\nEnter the number of the file you want to select: "))
    
    # Get the selected file name
    if user_input in files_dict:
        selected_file = files_dict[user_input]
        file_path = os.path.join(directory, selected_file)
        return file_path
    else:
        print("Invalid selection!")
        return None

def select_doc():
    file_path = get_files_in_directory('docs')
    if file_path:
        return f"{os.getcwd()}/{file_path}"

def select_all_docs():
    directory = 'docs'
    return [os.path.abspath('docs/'+f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
