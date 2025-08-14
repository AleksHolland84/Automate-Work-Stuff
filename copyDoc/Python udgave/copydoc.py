import shutil, os, re, datetime
from docx import Document

# program variables and meta
folder = 'indhold'
documentnavn = ''
base_file = 'template.docx'
subfolder = 'copied'
klasse = input('Hvilken klasse?: ')
elever = 'names.txt'
f_type = '.txt'

#Prompt for filename"
def file_name_prompt():
    prompt = 0
    while (prompt not in("y", "n")):
        prompt = input("Skal filnavn indeholde år? (y/n)").strip().lower()
    return prompt == "y"
    


path = '' # will contain path to subfolder

def dater():
    now = datetime.date.today()
    return now

def create_folder():
    global folder, subfolder, path
    folder = os.path.abspath(folder) # make sure path to folder is absolute
    new_folder_path = folder + '\\' + (subfolder + '_' + klasse) 
    if not os.path.exists(new_folder_path):
        os.mkdir(new_folder_path)
        path = new_folder_path
    else:
        path = new_folder_path


def create_list(filename, f_type):
    # takes a file as an argument and returns a list
    # contaning all the names in the file
    names = []
    filename = input("Filnavn på liste af elever?: ")
    
    filetype = re.compile(f'{f_type}$')
    mo = filetype.search(filename)

    try:
        if filename == '':
            filename = elever 
        elif mo:
            # if .txt in filename
            pass
        else: 
            filename = filename + '.txt'
        with open(filename, 'r', encoding='utf-8') as file:
            for name in file:
                names.append(name.strip(' \n\t'))
        return names
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        print(f"There's no file named: {filename}")
    except AttributeError as e:
        print(e)
        print('program error with regex at createlist() ')


def copy_frame(folder, base_file, new_path, name, date: bool = False):
    # copies a base_file and saves it as documentnavn + year + name of the name-argument
    foldername = os.path.abspath(new_path)

    # Check if filename should containe date:
    if date:
        new_file_path = foldername + f'\\{documentnavn} {dater()} {name}.docx'
    else: 
        new_file_path = foldername + f'\\{documentnavn} {name}.docx'
    try:
        if not os.path.exists(new_file_path): # check if file exists
            try:
                shutil.copy(os.path.join(folder, base_file), new_file_path)
                print(f'Created {os.path.basename(new_file_path)}')
            except FileNotFoundError as fnf_error:
                print(f"Can't find file at: {os.path.join(folder, base_file)}")
                shutil.copy(os.path.join(base_file), new_file_path)
                print(f'Created {os.path.basename(new_file_path)}')
        else:
            print(f"{os.path.basename(new_file_path)} ALLREADY EXISTS")
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        print('*** ERROR at copy_frame() ***')
        print(f'*** Error raised at {name} ***')





if __name__ == '__main__':
    elever = create_list(elever, f_type)

    # Check if file names shoudl include date
    include_date = file_name_prompt()

    create_folder()
    print("Sti til mappe: " + path)

    for elev in elever:
        copy_frame(folder, base_file, path, elev, include_date)