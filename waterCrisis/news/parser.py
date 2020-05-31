#!/usr/bin/env python3
"""
News parser.

TODO:
    Configure with argument of file or files
    Flag for doing request
    Requirements file
"""
import datetime
import textwrap

import requests
from bs4 import BeautifulSoup

NEWS_URI = "https://www.news24.com/SouthAfrica/water_crisis/"


class NewsItem(object):
    """Models an article on a news website."""

    def __init__(self, title, uri, description=None, publishedAt=None):
        self.title = title
        self.uri = uri
        self.description = description

        if publishedAt:
            self.publishedAt = datetime.datetime.strptime(
                publishedAt,
                "%Y-%m-%d %H:%M"
            ).date()
        elif uri.startswith("https://www.news24.com/"):
            # Expect all News24 artcles to have URI ending in "-YYYYMMDD".
            self.publishedAt = datetime.datetime.strptime(
                uri.rsplit("-", 1)[1],
                "%Y%m%d"
            ).date()
        else:
            self.publishedAt = None

    def __repr__(self):
        return "<NewsItem(title={title}, uri={uri},"\
            " description={description}, publishedAt=<{publishedAt}>".format(
            title=textwrap.shorten(self.title, width=40).__repr__(),
            uri=textwrap.shorten(self.uri, width=80).__repr__(),
            description=textwrap.shorten(self.description, width=10).__repr__()
                if self.description else self.description.__repr__(),
            publishedAt=self.publishedAt.__repr__()
        )


def main(fpath):
    with open(fpath) as f:
        # Get document as single multi-line string.
        html = f.read()

    #resp = requests.get(NEWS_URI, timeout=5)
    #html = resp.text

    soup = BeautifulSoup(html, 'html.parser')

    # TODO check other classes and "last" variation
    news_item_divs = soup.find_all('div', {'class': 'col300 news_item '})

    news_items_dict = {}

    for n in news_item_divs:
        article = n.h4
        assert article is not None, ("Could not find h4 on news div")

        uri = article.a['href']
        if uri not in news_items_dict:
            large_item = NewsItem(
                uri=uri,
                title=article.a.text,
                description=n.p.text,
                publishedAt=n.span.text
            )
            news_items_dict[uri] = large_item

        ul_items_list = n.ul
        if ul_items_list:
            for li in ul_items_list.find_all('li'):
                uri = li.a['href']

                if uri not in news_items_dict:
                    small_item = NewsItem(
                        uri=uri,
                        title=li.a.text,
                    )
                    news_items_dict[uri] = small_item

    for v in news_items_dict.values():
        print(v)


if __name__ == '__main__':
    main('var/news24.html')
