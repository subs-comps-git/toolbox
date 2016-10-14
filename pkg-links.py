#! /usr/bin/env python3
"""Makes links for compiled packages into a chosen directory"""


import argparse
import os
import pathlib


def get_files(source_path, topdown=True):
    """Return a list of directories and files"""
    return [[dirs, files] for dirs, subdirs, files in os.walk(source_path, topdown)
            if len(files) > 0]


def make_links(source, destination):
    """Creates symlinks for files in file_list. Accepts both relative and absolute paths"""
    package_files = get_files(source)
    # base_path = pathlib.Path(package_files[0][0]).parent
    base_path = pathlib.Path(source)
    # starting_dir = os.getcwd()
    index = len(base_path.parts)
    starting_dir = destination
    for path, files in package_files:
        source_path = pathlib.Path(path)
        destination = pathlib.Path(destination)
        if source_path.is_absolute():
            # relative_path = os.path.relpath(str(source_path), str(base_path))
            relative_path = '/'.join(source_path.parts[index:])
            destination_path = destination / relative_path
            # source_path = source
            relative_link = False
        else:
            relative_path = '/'.join(source_path.parts[index:])
            destination_path = destination / relative_path
            source_path = source_path.resolve()
            relative_link = True

        if not destination_path.exists():
            destination_path.mkdir()
            print('{} directory created.'.format(destination_path))

        os.chdir(str(destination_path))
        for file in files:
            link_file = pathlib.Path(file)
            # source_file = (source_path / file)
            if relative_link:
                source_file = source_path.resolve() / file
                source_file = os.path.relpath(str(source_file))
            else:
                source_file = (source_path / file)
            try:
                link_file.symlink_to(source_file)
                print('Link created: {} -> {}'.format(str(link_file), str(source_file)))
            except FileExistsError:
                print('{} exists, sckipping'.format(str(link_file)))
                pass
        os.chdir(starting_dir)


def remove_links(source, destination):
    package_files = get_files(source, topdown=False)
    starting_dir = destination
    base_path = pathlib.Path(source)
    index = len(base_path.parts)
    # print(base_path)
    for path, files in package_files:
        source_path = pathlib.Path(path)
        destination = pathlib.Path(destination)

        if source_path.is_absolute():
            relative_path = '/'.join(source_path.parts[index:])
            destination_path = destination / relative_path
        else:
            destination_path = destination / source_path
        try:
            os.chdir(str(destination_path))
            for file in files:
                link_file = pathlib.Path(file)
                try:
                    link_file.unlink()
                    print('{}: link removed'.format(str(link_file)))
                except FileNotFoundError:
                    print('{} not found, skipping'.format(str(link_file)))
            os.chdir(starting_dir)
            destination_path.rmdir()
            print('{}: directory removed.'.format(destination_path))
        except FileNotFoundError:
            print('{} not found, skipping'.format(str(destination_path)))
        except OSError:
            print('{} directory not empty, skipping'.format(destination_path))


def main():
    """Makes symbolic links for packages given it's source folder and a destination folder
    where links are to be made."""
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--install', action='store_true',
                       help='makes package links')
    group.add_argument('-r', '--remove', action='store_true',
                       help='removes package links')
    parser.add_argument('source_path', help='package directory')
    parser.add_argument('target_path', help='target directory for links')
    args = parser.parse_args()

    if args.install:
        make_links(args.source_path, args.target_path)
    elif args.remove:
        remove_links(args.source_path, args.target_path)
    else:
        print('Error: must select either {} or {} to process links.'.format('install', 'remove'))

if __name__ == '__main__':
    main()
