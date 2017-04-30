"""
Originally taken from:
http://www.pythoncentral.io/finding-duplicate-files-with-python/
Original Author: Andres Torres

Adapted to compute the md5sum of same size files.
"""
import os
import sys
import hashlib


def find_dups(parent_folder):
    # Dups in format {hash:[names]}
    dups = {}
    for dirName, subdirs, fileList in os.walk(parent_folder):
        print('Scanning %s...' % dirName)
        for filename in fileList:
            # Get the path to the file
            path = os.path.join(dirName, filename)
            # Calculate hash
            file_hash = hashfile(path)
            # Add or append the file path
            if file_hash in dups:
                dups[file_hash].append(path)
            else:
                dups[file_hash] = [path]
    return dups


def find_dup_size(parent_folder):
    # Dups in format {hash:[names]}
    dups = {}
    for dirName, subdirs, fileList in os.walk(parent_folder):
        print('Scanning %s...' % dirName)
        for filename in fileList:
            # Get the path to the file
            path = os.path.join(dirName, filename)
            # Calculate hash
            file_size = os.path.getsize(path)
            # Add or append the file path
            if file_size in dups:
                dups[file_size].append(path)
            else:
                dups[file_size] = [path]
    return dups


def find_dup_hash(file_list):
    print('Comparing: ')
    for filename in file_list:
        print('    {}'.format(filename))
    dups = {}
    for path in file_list:
        file_hash = hashfile(path)
        if file_hash in dups:
            dups[file_hash].append(path)
        else:
            dups[file_hash] = [path]
    return dups


# Joins two dictionaries
def join_dicts(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]


def hashfile(path, blocksize=65536):
    afile = open(path, 'rb')
    hasher = hashlib.sha1()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()


def print_results(dict1):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    if len(results) > 0:
        print('Duplicates Found:')
        print('The following files are identical. The name could differ, but the content is identical')
        print('___________________')
        for result in results:
            for subresult in result:
                print('\t\t%s' % subresult)
            print('___________________')

    else:
        print('No duplicate files found.')


def main(folders):
    dup_size = {}
    for i in folders:
        # Iterate the folders given
        if os.path.exists(i):
            # Find the duplicated files and append them to dup_size
            join_dicts(dup_size, find_dup_size(i))
        else:
            print('%s is not a valid path, please verify' % i)
            sys.exit()

    print('Comparing files with the same size...')
    dups = {}
    for dup_list in dup_size.values():
        if len(dup_list) > 1:
            join_dicts(dups, find_dup_hash(dup_list))
        print_results(dups)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        print('Usage: python dupFinder.py folder or python dupFinder.py folder1 folder2 folder3')
