"""Download RFC document from command line. """


import sys
import requests
import pydoc


def get_rfc(rfc_num):
    """Return an RFC document from the Internet.

    Args:
        rfc_num: Int. RFC document numner to request from website.

    Returns:
        A text version of the RFC document.
    """
    rfc_number = int(rfc_num)
    template = 'http://www.ietf.org/rfc/rfc{num}.txt'
    url = template.format(num=rfc_number)
    return requests.get(url).text


def main():
    """Downloads an RFC document and send it to the system pager.

    Raises:
        IndexError: An error occurs if an integer is not provided as first argument.
        ValueError: An arror occurs if first argument is not an integer.
    """
    try:
        pydoc.pager(get_rfc(sys.argv[1]))
    except (IndexError, ValueError):
        print('Must supply an RFC number as first argument')


if __name__ == '__main__':
    main()
