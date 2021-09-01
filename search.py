import os
import re
import win32api

def find_file(root_folder, rex, filters):
    results_list = []
    for root,dirs,files in os.walk(root_folder):
        for f in files:
            result = rex.search(f)
            for no in filters:
                result2 = no.search(f)
                if result and result2:
                    results_list.append(os.path.join(root, f))
        for d in dirs:
            result = rex.search(d)
            if result:
                for root,dirs,files in os.walk(os.path.join(root, d)):
                    for f in files:
                        for no in filters:
                            result = no.search(f)
                            if result:
                                results_list.append(os.path.join(root, f))
    return results_list

def find_file_in_all_drives(file_name,extensions_list):
    # results list
    result = []
    filters = []
    # blank field error
    if file_name.strip() == '':
        return '\nYou must enter something to search!!!'
    else:
        try:
            rex = re.compile(file_name)

            # blank extensions field
            if len(extensions_list) == 0:
                extensions_list = ['exe','doc','mp3','m4a','mp4','gif','png','jpeg','jpg','rar','zip','txt','pdf','html','wav','mov','xlsx','pptx','docx','avi','mkv']

            for no in extensions_list:
                sf = re.compile(no)
                filters.append(sf)
                
            # search in all drives
            for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
                result += find_file(drive, rex, filters)
            return result
        except:
            print('\nError!')

# Inputs
filename = input('Enter something to search in files (letters & numbers!): ')
extensions_input = input('Enter file extensions(With Spaces between!)(If you want to search with all extensions, leave this field blank!): ')

# convert str to list
extensions = extensions_input.split()

f = find_file_in_all_drives(filename,extensions)
print(f)

# Powered by Elman :)