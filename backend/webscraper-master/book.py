from product import Product

class Book(Product):

    def __init__(
        self,
        title,
        author,
        cover = None,
        ISBN10 = None,
        ISBN13 = None,
        pages = None,
        publisher = None,
        ):

        name = title + " by " + author
        description = None
        super(Book, self).__init__(name, description, cover)

        self.title = title
        self.author = author

        self.ISBN10 = ISBN10
        self.ISBN13 = ISBN13
        self.pages = pages
        self.publisher = publisher
        
        self.categories = []

    def add_category(category):
        self.categories.append(category)

    def __str__(self):
        return self.title + " by " + self.author

    def __eq__(self, other):
        if self.ISBN10 != None and other.ISBN10 != None:
            return self.ISBN10 == self.ISBN10
        elif self.ISBN13 != None and other.ISBN13 != None:
            return self.ISBN13 == self.ISBN13
        return False

