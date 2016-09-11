""" Recursively walk the current working directory looking for broken
symlinks. If any broken symlinks are found print out a report.
If none are found print out OK.

"""
import os


def find_links(folder):
    links = []
    broken = []
    for root, dirs, files in os.walk(folder):
        if root.startswith(('./.git', '.', '..')):
            # Ignore the .git directory.
            continue
        for filename in files:
            path = os.path.join(root, filename)
            if os.path.islink(path):
                target_path = os.readlink(path)
                # Resolve relative symlinks
                if not os.path.isabs(target_path):
                    target_path = os.path.join(os.path.dirname(path), target_path)
                if not os.path.exists(target_path):
                    links.append(path)
                    broken.append(path)
                else:
                    links.append(path)
            else:
                # If it's not a symlink we're not interested.
                continue
    return links, broken


def remove_links(link_list):
    try:
        for link in link_list:
            os.remove(link)
            print("Removed: {}".format(link))
    except FileNotFoundError as e:
        print(e)


def print_links(links, broken):
    if not broken:
        print("\nSymlinks found... {}".format(len(links)))
        print("OK... No broken links")
        # print(*links, sep='\n')
    else:
        print("broken symlink(s) found:")
        for link in broken:
            print("Broke: {}".format(link))


def main():

    folder = input("\nFolder to check: ")
    os.chdir(folder)
    cwd = os.getcwd()

    print("Checking for broken symlinks... {}".format(cwd))

    ok_links, broken_links = find_links(cwd)
    print_links(ok_links, broken_links)

    if broken_links:
        remove = input("\nRemove broken links? [default=N]: ") or "N"
        if remove[0] in 'Yy':
            remove_links(broken_links)
        else:
            print("Links NOT removed!")
    # else:
    #     print("Goodbye!")


if __name__ == '__main__':
    main()
