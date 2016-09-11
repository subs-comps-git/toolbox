import os


def make_file(filename, body=None):
    with open(filename, 'w') as f:
        f.write(body or filename)
    return


def make_example_dir(top):
    if not os.path.exists(top):
        os.mkdir(top)
    curdir = os.getcwd()
    os.chdir(top)

    make_file('common_file', 'this file is the same')
    os.symlink('common_file', 'file_link1')
    os.symlink('common_file', 'file_link2')
    os.symlink('common_file', 'file_link3')
    os.symlink('common_file', 'file_link4')

    os.chdir(curdir)
    return

if __name__ == '__main__':
    # os.chdir(os.path.dirname(__file__) or os.getcwd())
    os.chdir('/tmp')
    make_example_dir('example')
    print(os.getcwd())
