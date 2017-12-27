"""Program to download stock data from the yahoo YQL service"""


import requests
import urllib
import operator
import os


def mod_stock_list(filename):
    with open(filename, 'r') as fh:
        s = []
        for line in fh:
            sl = line.split('\t', maxsplit=2)
            s.append('\t'.join(sl[0:2]))
    with open(filename, 'w') as wh:
        wh.write('\n'.join(s))


def get_stock_list(filename):
    """Get list of stocks and attributes to download from file, *filename*.
    Column names come from description of flags in file."""

    # s = symbol(s) to lookup
    # f = flags (Symbol(s), price(l1), date(d1), time(t1), change(c1)) etc..
    # e = export??
    # names = column names
    table_query = {
        's': [],
        'f': [],
        'e': '.csv',
        'column_names': []
    }

    # Name the columns
    # table_columns = []

    # Intermediate list to help create table_query.
    # flags = []

    with open(filename, 'r') as fh:
        # stock_list = []
        # stock_list = [tuple(line.split('\t', maxsplit=2)) for line in fh]
        # for index, element in enumerate(stock_list):
        for element in fh:
            element = tuple(element.strip().split(None, 1))
            if not element or '#' in element[0]:
                break
            else:
                table_query['s'].append(element[0])

        # flags = stock_list[start + 1:]
        for element in fh:
            try:
                flag, name = tuple(element.strip().split(None, 1))
                if '#' in flag:
                    continue
                else:
                    table_query['column_names'].append(name)
                    table_query['f'].append(flag)
            except ValueError:
                continue

        table_query['s'] = ','.join(table_query['s'])
        table_query['f'] = ''.join(table_query['f'])

    return table_query


def build_outside_query(yql_query_function):
    def wrapper(*args, **kwargs):
        query = yql_query_function(*args, **kwargs)
        # payload for the final url, this is the fully built and encoded query sent to yahoo.
        url_payload = {
            'q': query,
            'format': 'json'
        }

        baseurl = "https://query.yahooapis.com/v1/public/yql"
        # Safe set to '', otherwise '/' characters in the query will not be encoded.
        # quote_via used to set quote instead of quote_plus.
        return '{base}?{query}'.format(
            base=baseurl,
            query=urllib.parse.urlencode(url_payload, safe='', quote_via=urllib.parse.quote)
        )
    return wrapper


@build_outside_query
def build_yql_query(query_data):
    """Returns a properly formatted url needed for a Yahoo YQL query"""
    base_table_url = 'http://download.finance.yahoo.com/d/quotes.csv?'

    # Parse the dictionary (query) as part of URL but do NOT encode ','.
    # Prevents double encoding down the line.
    column_names = query_data.pop('column_names')
    encoded_query = urllib.parse.urlencode(query_data, safe=',')

    # Combine base url with encoded query and yql statement
    table_url = '{base}{query}'.format(base=base_table_url, query=encoded_query)
    return "select * from csv where url='{url}' and columns='{columns}'".format(
        url=table_url,
        columns=','.join(column_names)
    )

    # # payload for the final url, this is the fully built and encoded query sent to yahoo.
    # url_payload = {
    #     'q': yql_query,
    #     'format': 'json'
    # }

    # baseurl = "https://query.yahooapis.com/v1/public/yql"

    # # Safe set to '', otherwise '/' characters in the query will not be encoded.
    # # quote_via used to set quote instead of quote_plus.
    # return '{base}?{query}'.format(
    #     base=baseurl,
    #     query=urllib.parse.urlencode(url_payload, safe='', quote_via=urllib.parse.quote)
    # )


def dow10_highest_yielding(json_data):
    # Convert strings to floats for appropriate fields.
    for row in json_data:
        for key, value in row.items():
            if key in ['price', 'div_share', 'yield', 'open', 'high', 'low']:
                row[key] = float(row[key])

    # sort by yield
    yield_sorted = sorted(json_data, key=operator.itemgetter('yield'), reverse=True)

    # List of 10 highest yielding dow stocks
    dow10 = [row for index, row in enumerate(yield_sorted) if index < 10]
    yield_price_sorted = sorted(dow10, key=operator.itemgetter('price'))
    return yield_price_sorted


def foolish_four(dow10_data):
    return dow10_data[1:5]


def invest_fool_four(amt, ff_data):

    total = 0
    # investment = amt
    for index, element in enumerate(ff_data):
        name = element['symbol']
        price = element['price']
        if index == 0:
            ratio = 2 / 5 * amt
            shares = round(ratio / price)
            cost = round(price * shares, 2)
        else:
            ratio = 1 / 5 * amt
            shares = round(ratio / price)
            cost = round(price * shares, 2)
        print('{symbol:>11}{price:>11}{shares:>11}{cost:>11}'.format(
            symbol=name,
            price=price,
            shares=shares,
            cost=cost))
        total += cost
    print('Total cost:{:>33}'.format(round(total, 2)))


def main():
    """Download stock data from Yahoo finance using Yahoo's YQL API"""

    dev = os.getenv("DEV")
    file_path = "src/python/toolbox/finance"
    filename = os.path.join(dev, file_path, "stock_list.txt")

    # Build URL to pass to the YQL statement
    table_data = get_stock_list(filename)
    url = build_yql_query(table_data)
    r = requests.get(url)
    try:
        rows = r.json()['query']['results']['row']

    # Print results
        print('Top 10 highest yielding Dow stocks sorted by yield and price')
        print('{:>11}{:>11}{:>11}{:>11}'.format('symbol', 'price', 'div_share', 'yield'))
        print('{0:>11}{0:>11}{0:>11}{0:>11}'.format('-----'))
        price_dow = dow10_highest_yielding(rows)

        for row in price_dow:
            print('{symbol:>11}{price:>11}{div_share:>11}{yield:>11}'.format(**row))
        print("\nUrl: {url}".format(url=r.url))
    except TypeError:
        print(r.json())


if __name__ == '__main__':
    main()
