import requests
from bs4 import BeautifulSoup
import sys
import codecs
import lxml
import pandas as pd
from book import Book
from product import Listing
from multiprocessing import Pool
from database import BookDatabase

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

class BarnesNobleReader:
    """
    Interface for scraping product data from Barnes and Noble
    website.

    """

    vendor = 'Barnes & Noble'
    base_url = 'https://www.barnesandnoble.com'

    def __init__(self):
        pass

    @classmethod
    def read_category(cls, url):
        base_url = 'https://www.barnesandnoble.com'
        html = requests.get(url).content
        soup = BeautifulSoup(html, "lxml")

        groups = soup.find('div', attrs={'id':'searchGrid'}).find_all(attrs={'class':' '})
        groups = [b['href'] for b in groups]
        print(groups)

    @classmethod
    def read_book_page(cls, html, url):
        """
        Scrapes a single book page and returns a book object
        along with a listing

        """
        soup = BeautifulSoup(html, "lxml")

        title = soup.find(attrs={'itemprop':'name'}).text
        author = soup.find(attrs={'itemprop':'author'}).text

        info = soup.find(attrs={'id':'productDetail-container'})
        try:
            price = info.find(attrs={'id':'pdp-cur-price'}).text
            old_price = info.find(attrs={'class':'old-price'}).text
        except AttributeError:
            pass

        details = pd.read_html(html, index_col=0)[0]

        return (Book(title=title, author=author), 
                Listing(vendor=cls.vendor, price=price, url=url))

    @classmethod
    def read_page(cls, url):
        """
        Downloads html file from page url, determines the type of product,
        then feeds the html file to the appropiate scraper

        Product Types: Book, Movie, etc

        """
        html = requests.get(url).content
        soup = BeautifulSoup(html, "lxml")
        try:
            cat = soup.find(attrs={'class':'breadCrumbNav'}).find_all('li')[1].contents[0].text
        except AttributeError:
            return None

        if cat == 'Books':
            return cls.read_book_page(html, url)
        return None

    @classmethod
    def crawl_sitemap(cls):
        """
        Traverses the entire website and scrapes all product listings
        
        """
        url = 'https://www.barnesandnoble.com/sitemap.xml'
        html = requests.get(url).content
        soup = BeautifulSoup(html, "xml")

        links = soup.find_all('sitemap')
        links = [l.text.strip() for l in links]
        links = links[0:1]
        print(links)
        book_urls = []
        for l in links:
            print(l)
            soup = BeautifulSoup(requests.get(l).content, 'xml')
            book_urls = book_urls + [b.loc.text for b in soup.find_all('url')]

        book_urls = book_urls[100:200]

        p = Pool(5)
        books = p.map(cls.read_page, book_urls)
        return books

if __name__ == '__main__':

    url = 'https://www.barnesandnoble.com/b/books/science-fiction-fantasy/star-wars-fiction/_/N-29Z8q8Z1847'
    url2 = 'https://www.barnesandnoble.com/w/last-shot-daniel-jos-older/1127969204?ean=9781984800466#/'
    url3 = 'https://www.barnesandnoble.com/w/dvd-vietnam-war-a-film-by-ken-burns-lynn-novick/31120553'
    url4 = 'https://www.barnesandnoble.com/w/fahrenheit-451-ray-bradbury/1100383286?ean=9781451673319#/'
    url5 = 'https://www.barnesandnoble.com/w/three-days-in-moscow-bret-baier/1126973079?ean=9780062748362#/'

    test_links = [url2,url3,url4,url5]

    reader = BarnesNobleReader()    
    
    p = Pool(10)
    books = p.map(reader.read_page, test_links)

    db = BookDatabase()

    for b in books:
        if b is not None:
            print(b[0])
            #db.add_listing(b[0], b[1])
    """
    db = BookDatabase()

    books = reader.crawl_sitemap()
    for b in books:
        if b is not None:
            print(b[0])
            db.add_listing(b[0], b[1])
    """