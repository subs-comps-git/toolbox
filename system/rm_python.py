"""Removes links from old versions of python on OSX.

Useful for removing links between differing python versions without deleting
python itself.
"""

import os
import filecmp
import argparse


def get_options():
    """Get commandline options from sys.argv and return dictionary of arguments.

    Args:
        -d: Optional boolean argument to flag links for removal.
        version: A string version number of python to view or remove.
        target: A path string containing symlinks to python binaries, e.g. /usr/bin.
    Returns:
        A dictionary mapping of arguments.
    """
    parser = argparse.ArgumentParser(description="Remove old versions of python from OSX")
    parser.add_argument("-d", help="delete links", action="store_true")
    parser.add_argument("version", help="Python version, e.g. 2.6", action="store", type=str)
    parser.add_argument("target", help="Location of python symlinks, e.g. /usr/bin.",
                        action="store", type=str)
    return vars(parser.parse_args())


def print_links(links):
    """print matched links in *target*.

    Args:
        links: A list of links.
    """
    print("\nMatches:")
    for f in links:
        print(f, end='')
        print("  {0}".format(os.readlink(f)))


def find_links(src, dst):
    """Find symlinks and return list.

    Args:
        src: A string containing the path to python.
        dst: A path string containing symlinks to python binaries, e.g. /usr/bin.
    Returns:
        A list of symlink path strings.
    """
    dir_compare = filecmp.dircmp(src, dst)
    links = [os.path.join(dst, link) for link in dir_compare.common_files
             if os.path.islink(os.path.join(dst, link))]

    return links


def rm_links(links):
    """Remove symlinks from *target* location and print removals.

    Args:
        links: A list of symlink path strings.
    Returns:
        Prints removed symlinks.
    """
    try:
        for link in links:
            os.remove(link)
            print("{link} removed".format(link=link))
    except OSError as e:
        print("\nCannot remove link!")
        print("Permissions Error ({0}): {1}".format(e.errno, e.strerror))


def main():
    """Program to remove symlinks from old versions of python in *target* directory."""
    base = '/System/Library/Frameworks/Python.framework/Versions'

    args = get_options()
    srcpath = os.path.join(base, args['version'], 'bin')
    delete, target_path = args['d'], args['target']

    if delete:
        links = find_links(srcpath, target_path)
        rm_links(links)
    else:
        links = find_links(srcpath, target_path)
        print_links(links)


if __name__ == '__main__':
    main()
