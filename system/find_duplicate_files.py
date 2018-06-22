"""Finds duplicate files


"""


import xxhash
import sys
import os
import pprint


def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes."""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk


def get_hash(filename, first_chunk=False, myhash=xxhash.xxh64):
    """Hash files to verify if they're different."""
    hashobj = myhash()
    file_object = open(filename, 'rb')

    if first_chunk:
        hashobj.update(file_object.read(1024))
    else:
        for chunk in chunk_reader(file_object):
            hashobj.update(chunk)
    hashed = hashobj.hexdigest()

    file_object.close()
    return hashed


def sort_by_size(paths):
    hashes_by_size = {}
    for path in paths:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                try:
                    file_size = str(os.path.getsize(full_path))
                except OSError:
                    # Not accessible (permissions, etc)
                    pass

                duplicate = hashes_by_size.get(file_size)
                if duplicate:
                    hashes_by_size[file_size].append(full_path)
                else:
                    hashes_by_size[file_size] = []  # create list for this file size
                    hashes_by_size[file_size].append(full_path)
    return hashes_by_size


def hash_files(sorted_files, first_chunk=False):
    hashes_full = {}
    for _, files in sorted_files.items():
        if len(files) < 2:
            continue

        for filename in files:
            small_hash = get_hash(filename, first_chunk=False)

            duplicate = hashes_full.get(small_hash)
            if duplicate:
                hashes_full[small_hash].append(filename)
            else:
                hashes_full[small_hash] = []
                hashes_full[small_hash].append(filename)
    return hashes_full


def check_for_duplicates(paths, myhash=xxhash.xxh64):
    """Return a dictionary of duplicate files


    """
    hashes_by_size = sort_by_size(paths)
    hashes_full = hash_files(hashes_by_size)
    duplicates = {}

    for _, files in hashes_full.items():
        if len(files) > 1:
            first_file = files.pop(0)
            first_file = os.path.basename(first_file)
            duplicates[first_file] = []
            for file in files:
                print(f'{file} is a duplicate of {first_file}')
                duplicates[first_file].append(file)

    return duplicates


def main():
    if sys.argv[1:]:
        pprint.pprint(check_for_duplicates(sys.argv[1:]))
    else:
        print('Pass the paths to check as parameters to the script.')


if __name__ == '__main__':
    main()
