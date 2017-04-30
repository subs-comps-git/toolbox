"""Removes old versions of python on OSX.

"""

import os
import filecmp
import sys
import getopt


def usage():
    print("Usage: rm_python.py [options] ... [src path] [dst path]")
    print("Options:")
    print("{0:>10}{1:>8} : {2:<20}".format("-h", " ", "Usage"))
    print("{0:>10}{1:>8} : {2:<20}".format("-p", " ", "Print links"))
    print("{0:>10}{1:>8} : {2:<20}".format("-r", " ", "Remove links"))
    print("{0:>10}{1:>8} : {2:<20}".format("-s", "--src=", "Source path"))
    print("{0:>10}{1:>8} : {2:<20}".format("-d", "--dst=", "Destination path"))


# def print_links(d1, d2, common, links, diff):
def print_links(d1, d2, common):
    # print("\nAll files:")
    # for f in common:
    #     print("{0}".format(os.path.join(d2, f)))
    #
    # print("\nLinks:")
    # for f in links:
    #     print("{0}".format(os.path.join(d2, f)))
    #
    # print("\nDifference:")
    # for f in diff:
    #     print("{0}".format(os.path.join(d2, f)))

    match, mismatch, errors = filecmp.cmpfiles(d1, d2, common, shallow=False)
    print("\nMatch:")
    for f in match:
        if os.path.islink(os.path.join(d2, f)):
            print("link: {0}".format(os.path.join(d2, f))),
            print("{0:>15}".format(os.readlink(os.path.join(d2, f))))
        elif os.path.isfile(os.path.join(d2, f)):
            print("file: {0}".format(os.path.join(d2, f)))

    print("\nMismatch:")
    for f in mismatch:
        if os.path.islink(os.path.join(d2, f)):
            print("link: {0}".format(os.path.join(d2, f)))
            print("{0:>15}".format(os.readlink(os.path.join(d2, f))))
        elif os.path.isfile(os.path.join(d2, f)):
            print("file: {0}".format(os.path.join(d2, f)))
    print("\nErrors", errors)


def find_links(d1, d2):
    d1_contents = set(os.listdir(d1))
    d2_contents = set(os.listdir(d2))
    common = list(d1_contents & d2_contents)
    common_files = [f for f in common
                    if os.path.isfile(os.path.join(d2, f))]

    links = [f for f in common
             if os.path.islink(os.path.join(d2, f))]
    # cf = set(common_files)
    # cl = set(links)
    # diff = list(cf - cl)

    return d1, d2, common_files, links


def rm_links(directory, links):
    try:
        for link in links:
            os.remove(os.path.join(directory, link))
            print("%s removed" % os.path.join(directory, link))
    except OSError as e:
        print("\nCannot remove link!")
        print("Permissions Error ({0}): {1}".format(e.errno, e.strerror))


def main(argv):
    base = '/System/Library/Frameworks/Python.framework/Versions'
    version = ''
    bindir = 'bin'
    # srcpath = os.path.join(base, version, bindir)
    dstpath = ''
    view_links = False
    delete_links = False
    try:
        opts, args = getopt.getopt(argv, "prhs:d:", ["src=", "dst="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-s", "--src"):
            version = arg
        elif opt in ("-d", "--dst"):
            dstpath = arg
        elif opt == "-p":
            view_links = True
        elif opt == "-r":
            delete_links = True

    srcpath = os.path.join(base, version, bindir)

    if view_links:
        # d1, d2, common, links, diff = find_links(srcpath, dstpath)
        d1, d2, common, links = find_links(srcpath, dstpath)
        print_links(d1, d2, common)
        # print_links(d1, d2, common, links, diff)

    elif delete_links:
        _, d2, _, links = find_links(srcpath, dstpath)
        rm_links(d2, links)
    else:
        usage()
        sys.exit()


if __name__ == '__main__':
    main(sys.argv[1:])
