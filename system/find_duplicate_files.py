"""Finds duplicate files


"""


import xxhash
import sys
import os


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


def hash_files(sorted_files):
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
    hashes_by_size = {}
    hashes_on_1k = {}
    hashes_full = {}

    for path in paths:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                try:
                    file_size = os.path.getsize(full_path)
                except OSError:
                    # Not accessible (permissions, etc)
                    pass

                duplicate = hashes_by_size.get(file_size)
                if duplicate:
                    hashes_by_size[file_size].append(full_path)
                else:
                    hashes_by_size[file_size] = []  # create list for this file size
                    hashes_by_size[file_size].append(full_path)

    # For all files with same file size, get hash on 1st 1k bytes.
    for _, files in hashes_by_size.items():
        if len(files) < 2:
            continue

        for filename in files:
            small_hash = get_hash(filename, first_chunk=True)

            duplicate = hashes_on_1k.get(small_hash)
            if duplicate:
                hashes_on_1k[small_hash].append(filename)
            else:
                hashes_on_1k[small_hash] = []
                hashes_on_1k[small_hash].append(filename)

    # for all files with hash on 1st 1k bytes, get hash on full file - collisions are duplicates
    for _, files in hashes_on_1k.items():
        if len(files) < 2:
            continue

        for filename in files:
            full_hash = get_hash(filename, first_chunk=False)

            duplicate = hashes_full.get(full_hash)
            if duplicate:
                print(f'Duplicate found: {filename} and {duplicate}')
            else:
                hashes_full[full_hash] = filename
                print(f'\nNew hash....{full_hash}')
                print(f'comparing file {filename}')
                print('------------------------')


def main():
    if sys.argv[1:]:
        check_for_duplicates(sys.argv[1:])
    else:
        print('Pass the paths to check as parameters to the script.')


if __name__ == '__main__':
    main()
