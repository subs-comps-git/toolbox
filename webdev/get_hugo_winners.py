"""Program to download Hugo award winners list for novels. """


import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    """Download html content from wikipedia url

    Args:
        url (str): Wikipedia url for Hugo award winners.

    Returns:
        str: website content.
    """
    return requests.get(url).text


def make_soup(html_data, parser):
    """Parse website content into beautiful soup object

    Args:
        html_data (str): website content.
        parser (str): name of html parser.

    Returns:
        obj: beautiful soup object.
    """
    return BeautifulSoup(html_data, parser)


def make_book_list(bs4_obj, runners_up=False):
    """List of Hugo award winners and runners up.

    Args:
        bs4_obj (bs4.element.ResultSet): A list of bs4 elements.
        runners_ip (bool): Toggles inclusion of runners up in the list.

    Returns:
        list: A list of hugo award winners and runners up.

    Raises:
        AttributeError: Occurs if the table header is inherited.
    """
    table = bs4_obj.find('table', attrs={"class": "sortable wikitable"})
    if runners_up:
        rows = table.find_all('tr')[1:]
    else:
        rows = table.find_all('tr', style=True)

    year = None
    book = None
    book_list = []
    for row in rows:
        year = row.th.a.text if row.th else year
        columns = row.find_all('td')[:2]
        author = columns[0].span.text
        book = len(columns) > 1 and columns[1].i.text or book
        book_list.append([year, author, book])
    return book_list


def print_books(book_list):
    """Print list of books.

    Args:
        book_list (list): list of books returned from make_book_list.
    """
    for row in book_list:
        print('{year}, {auth}, {book}'.format(
            year=row[0],
            auth=row[1],
            book=row[2])
        )


def write_csv(filename, obj):
    """Write book list to csv file.

    Args:
        filename (str): Name of file to write.
        obj (list): List of books returned from make_book_list.
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Year', 'Author', 'Novel'])
        for row in obj:
            writer.writerow([row[0], row[1], row[2]])


def main():
    """This program downloads, parses, and writes to csv a list of authors who have
    won the Hugo award for best novel and also the runners up.
    """
    # Download data
    url = 'https://en.wikipedia.org/wiki/Hugo_Award_for_Best_Novel'
    html_data = get_html(url)

    # Parse and print.
    runners_up = False
    soup = make_soup(html_data, 'html5lib')
    hugos = make_book_list(soup, runners_up=runners_up)
    print_books(hugos)

    # Write to csv file
    write = False
    if write:
        write_csv('hugo_list.csv', hugos)


if __name__ == '__main__':
    main()
