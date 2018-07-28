import requests
from lxml import html

def get_season(year):
    sample = 'http://www.espncricinfo.com/ci/engine/series/index.html?'
    params = {'season': year, 'view': 'season'}
    get = lambda x: (x.attrib['data-series-id'], x.attrib['data-summary-url'])
    page = requests.get(sample, params=params)
    tree = html.fromstring(page.content)
    sections = tree.xpath('//section[@class="series-summary-block collapsed"]')
    series, url = zip(*(map(get, sections)))
    return (series, url)

def get_match_nos(url):
    base = 'http://www.espncricinfo.com'
    page = requests.get(base+url)
    tree = html.fromstring(page.content)
    hrefs = tree.xpath('//span[@class="match-no"]/a')
    get_text_match_no = lambda x: x.attrib['href'].split('/')[6]
    match_nos = list(map(get_text_match_no, hrefs))
    return match_nos