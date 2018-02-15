import os
import codecs


# Each website is a separate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


# Create queue and crawled files (if not created)
def create_data_files(project_name, base_url):
    queue = os.path.join(project_name , 'queue.txt')
    crawled = os.path.join(project_name,"crawled.txt")
    extracted_data_file = os.path.join(project_name,"extracted_data_file.txt")
    NameFile = os.path.join(project_name,"NameFile.txt")
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')
    if not os.path.isfile(extracted_data_file):
        write_file(extracted_data_file, '')
    if not os.path.isfile(NameFile):
        write_file(NameFile, '')


# Create a new file
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


# Add data onto an existing file
def append_to_file(data,path ):
    with open(path, 'a') as file:
        file.write(data + '\n')


# Delete the contents of a file
def delete_file_contents(path):
    open(path, 'w').close()


# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results

def DataFile_to_set(file_name):
    results = set()
    data = ""
    f = codecs.open(file_name, 'r','utf-8')
    for char in f.read():
        if char != '$':
            data += char
        else:
            data += '$'
            results.add(data)
            data = ""
    f.close()
    return results



# Iterate through a set, each item will be a line in a file
def set_to_file(links, file_name):
    with codecs.open(file_name,"w","utf-8") as f:
        for l in sorted(links):
            f.write(l+"\n")

def dataset_to_file(links, file_name):
    with codecs.open(file_name,"w","utf-8") as f:
        for l in links:
            f.write(l+"\n")
