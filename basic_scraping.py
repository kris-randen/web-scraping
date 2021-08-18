import requests
from bs4 import BeautifulSoup
import pandas as pd


APPLE_APP_REVIEWS = 'https://apps.apple.com/us/app/myfitnesspal/id341232718#see-all/reviews'
TESLA_WIKIPEDIA = 'https://en.wikipedia.org/wiki/Tesla,_Inc.'


HTML_PARSER = 'html.parser'
TESLA_TABLE_SELECTOR = '#mw-content-text > div.mw-parser-output > table:nth-child(320)'
SPACE = ' '
T_BODY = 'tbody'
T_ROW = 'tr'
T_DATA = 'td'


def soupify(text):
    return BeautifulSoup(text, features=HTML_PARSER)

def save():
    # Download the HTML from URL
    html_apple = requests.get(APPLE_APP_REVIEWS)
    html_tesla = requests.get(TESLA_WIKIPEDIA)

    # Parse the HTML with BeautifulSoup and create a soup object
    soup_apple = soupify(html_apple.text)
    soup_tesla = soupify(html_tesla.text)

    # Save a local copy
    with open('apple.html', 'w') as file_apple, \
            open('tesla.html', 'w') as file_tesla:
        file_apple.write(soup_apple.prettify())
        file_tesla.write(soup_tesla.prettify())


def load():
    # Load the local copy
    with open('apple.html', 'r') as file_apple, \
            open('tesla.html', 'r') as file_tesla:
        soup_apple = soupify(file_apple)
        soup_tesla = soupify(file_tesla)

    return soup_apple, soup_tesla


def clean(string):
    if not string:
        return '0'
    index = string.find('_')
    return string[:index] if index != -1 else string

def process():
    import re

    reg_00 = re.compile('_\[\w\]')
    reg_01 = re.compile('[\n\r\s]+')
    reg_02 = re.compile('_\[\a-zA-Z\d\]+')
    soup_apple, soup_tesla = load()
    table_tesla = soup_tesla.select(TESLA_TABLE_SELECTOR + SPACE + T_BODY)[0]
    table_tesla_head = table_tesla.select('tr th')


    # print(table_tesla_other_head)
    # print(table_tesla)

    table_columns = []
    for element in table_tesla_head:
        column_label = element.get_text(separator=' ', strip=True)
        column_label = column_label.replace(' ', '_')
        column_label = reg_02.sub('', column_label)
        table_columns.append(column_label)

    print(table_columns)

    table_rows = table_tesla.select(T_ROW)

    table_data = []

    for index, row in enumerate(table_rows):
        if index == 0:
            continue
        table_data.append([clean(reg_01.sub('_', value.text.strip())) for value in row.select(T_DATA)])

    import pprint

    print(table_data)
    pd.set_option('display.max_columns', None)
    df = pd.DataFrame(table_data, columns=table_columns)
    pprint.pp(df)


if __name__ == '__main__':
    process()




