import requests
from bs4 import BeautifulSoup
import lxml

from book import Book
from product import Listing
import time

class BAMReader:
    """
    Interface for scraping product data from Books a Million
    website.

    """

    vendor = 'Books a Million'
    base_url = 'www.booksamillion.com'

    @classmethod
    def read_book_page(cls, html, url):

        soup = BeautifulSoup(html, "lxml")

        title = soup.find(attrs={'class':'details-title-text'}).contents[0].text
        authors = soup.find(attrs={'class':'details-author-text'}).find_all('a')
        authors = [a.text for a in authors]

        price_info = soup.find(attrs={'class':'price-block-binding'})

        try:
            sale_price = price_info.find(attrs={'class':'details-title-text'}).find('strong').text
        except AttributeError:
            return None

        try:
            retail_price = price_info.find(attrs={'class':'details-retail-price'}).find('strike').text
        except AttributeError:
            pass

        cover = soup.find(attrs={'id':'details-image-container'}).find('a')['href']

        details = {}
        table = soup.find(attrs={'name':'details'}).parent.find_all('li')
        for row in table:
            details[row.contents[0].text] = row.contents[1][2:]

        return (Book(title=title, author=authors[0], cover=cover), 
                Listing(vendor=cls.vendor, price=sale_price, url=url))

    @classmethod
    def read_page(cls, url):
        try:
            html = requests.get(url, timeout=5).content
            soup = BeautifulSoup(html, "lxml")

            if True:
                return cls.read_book_page(html, url)
            else:
                return None
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
            return None

    @classmethod
    def crawl_from_xml(cls, file):
        file = open(file)
        soup = BeautifulSoup(file, 'xml')
        links = [l.loc.text for l in soup.find_all('url')]

        links = links[0:100]
        books = []
        for l in links:
            print(l)
            books.append(cls.read_page(l))
            time.sleep(2.5)

        books[:] = (b for b in books if b != None)

        return books

    @classmethod
    def crawl_sitemap(cls):
        pass

if __name__ == '__main__':

    url0 = 'http://www.booksamillion.com/p/Animal-Farm/George-Orwell/9780151010264'
    reader = BAMReader()
    #b = reader.read_page(url0)
    #print(b[0].image)

    xml_path = 'C:\\Users\\blins\\Documents\\Projects\\Ultimate Shopping Website\\scraper\\data\\sitemap_1_0.xml'
    book = reader.crawl_from_xml(xml_path)

