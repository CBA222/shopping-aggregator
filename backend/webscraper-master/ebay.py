from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
from product import Product, Listing

class EbayReader:

    def __init__(self, appid):
        self.api = Finding(appid=appid, config_file=None)
        self.vendor = 'EBAY'

    def get_products_by_category(self, categoryID, count):
        response = self.api.execute('findItemsByCategory', {'categoryId': categoryID})

        if count >= int(response.reply.paginationOutput.totalEntries):
            count = int(response.reply.paginationOutput.totalEntries)

        num_pages = int(count / 100)
        product_list = []

        for page_number in range(1, num_pages):
            params = {
                'categoryId': categoryID,
                'outputSelector': 'PictureURLLarge',
                'paginationInput': {
                    'entriesPerPage': 100,
                    'pageNumber': page_number
                }
            }
            response = self.api.execute('findItemsByCategory', params)
        
            for item in response.reply.searchResult.item:
                try:
                    image=item.pictureURLLarge
                except AttributeError:
                    try:
                        image=item.galleryPlusPictureURL
                    except AttributeError:
                        try:
                            image=item.galleryURL
                        except AttributeError:
                            image=None
                product = Product(
                    name=item.title,
                    description=None,
                    image=image
                )
                listing = Listing(
                    vendor=self.vendor,
                    price=item.sellingStatus.currentPrice.value,
                    url=item.viewItemURL
                )
                product_list.append( (product, listing) )

        return product_list

if __name__ == '__main__':
    appid = 'BrianLin-fullshel-PRD-f7141958a-eee81537'
    reader = EbayReader(appid)
    reader.get_products_by_category(1, 2)