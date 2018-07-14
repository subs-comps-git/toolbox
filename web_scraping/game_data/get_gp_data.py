"""Download data from swgoh.gg and prepare data to export to spreadsheet


"""


from bs4 import BeautifulSoup
import requests
import requests_cache
import datetime


def get_html(url):
    """Download html content from Wikipedia url
    https://swgoh.gg/g/11008/hansoloshotfirst/gp/

    Args:
        url (str): Wikipedia url for Hugo award winners.

    Returns:
        str: website content.
    """
    expire = datetime.timedelta(hours=1)
    requests_cache.install_cache(expire_after=expire)
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


def make_gp_list(bs4_obj):
    """Returns a list of GP by character name


    """
    gp_list = []
    table_rows = bs4_obj.tbody('tr')
    for data in table_rows:
        gp_data = data.find_all('td')
        name = gp_data[0].strong.text
        total_gp = int(gp_data[1].text)
        char_gp = int(gp_data[2].text)
        ship_gp = int(gp_data[3].text)
        gp_list.append((name, total_gp, char_gp, ship_gp))

    return gp_list
