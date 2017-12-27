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
        parser (str): name of parser.

    Returns:
        obj: beautiful soup object.
    """
    return BeautifulSoup(html_data, parser)


def make_book_list(obj):
    """List of Hugo award winners and runners up.

    Args:
        obj (bs4.element.ResultSet): A list of bs4 elements.

    Returns:
        list: A list of hugo award winners and runners up.

    Raises:
        AttributeError: Occurs if the table header is inherited.
    """
    year = None
    book = None
    book_list = []
    for row in obj[1:]:
        try:
            year = row.th.a.text,
            table_data = row.find_all('td')
            author = table_data[0].a.text
            book = table_data[1].a.text
            book_list.append([year[0], author, book])
        except AttributeError:
            text = row.get_text()
            author = row.td.a.text
            book1 = text.split('\n')[2]
            book = book1 if book1 else book
            book_list.append([year[0], author, book])
    return book_list


def print_books(obj):
    """Print list of books.

    Args:
        obj (list): list of books returned from make_book_list.
    """
    for row in obj:
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
    url = 'https://en.wikipedia.org/wiki/Hugo_Award_for_Best_Novel'
    html_data = get_html(url)

    soup = make_soup(html_data, 'html5lib')
    tables = soup.find_all('table', attrs={"class": "sortable wikitable"})
    rows = tables[0].find_all('tr')

    hugos = make_book_list(rows)
    print_books(hugos)
    write_csv('hugo_list.csv', hugos)


if __name__ == '__main__':
    main()
