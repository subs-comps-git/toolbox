#! /usr/bin/env python3
"""Python style grep"""

import sys
import re
import fileinput


def grep_py(args):
    """Searches for pattern in files given on commandline
    and prints matches to standard out.

    Args:
        args: commandline arguments.
    """

    try:
        search_string = args[1]
        with fileinput.input(args[2:]) as infile:
            matches = [(infile.filename(), infile.filelineno(), line)
                       for line in infile
                       if re.search(search_string, line, re.IGNORECASE)]

        if len(args[2:]) > 1:
            for file_name, line_number, line in matches:
                print('{file_name}: ({number}):   {match}'.format(
                    file_name=file_name,
                    number=line_number,
                    match=line),
                    end='')
        else:
            print(*matches, sep='')
    except FileNotFoundError:
        print('{program_name}: {file_name}: No such file or directory'.format(
            program_name=args[0],
            file_name=args[2]
            ))
        sys.exit(-2)
    except KeyboardInterrupt:
        sys.exit(-3)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        sys.exit(grep_py(sys.argv))
    else:
        sys.exit(-1)
