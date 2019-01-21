import requests
from bs4 import BeautifulSoup
import sys
import codecs
import lxml

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)



def read_category(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, "lxml")

    groups = soup.find(attrs={'class':'product-card-grid--all-groups'}).contents
    print(groups)

if __name__ == '__main__':
    url = 'https://oldnavy.gap.com/browse/category.do?cid=5226&sop=true'
    read_category(url)