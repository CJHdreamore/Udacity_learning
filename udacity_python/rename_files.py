import os
def rename_files():
    # get all file names from a folder
    file_list = os.listdir(r"C:\Users\CJH\Downloads\alphabet\alphabet\secrete_message")
    # for each file,rename filenames
    #print(file_list)
    saved_path = os.getcwd()
    print("Current Working Directory is "+ saved_path)
    os.chdir(r"C:\Users\CJH\Downloads\alphabet\alphabet\secrete_message")
    for file_name in file_list:
       os.rename(file_name,file_name.translate(None,"0123456789"))
    print(file_list)
    os.chdir(saved_path)
rename_files()
