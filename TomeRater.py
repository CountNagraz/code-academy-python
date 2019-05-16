# Main class
class TomeRater(object):
    def __init__(self):
        self.users = {} # email:user
        self.books = {} # book:number of users who read it

    def create_book(self, title, isbn):
        return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating = None):
        user = self.users.get(email, None)

        if(user is None):
            print("No user with email {}!".format(email))
            return
        
        user.read_book(book, rating)
        book.add_rating(rating)
        
        if(book in self.books.keys()):
            self.books[book] += 1
        else:
            # Make sure that new book has a unique ISBN
            if(self.isbn_already_exists(book.isbn)):
                print("Book with ISBN: {} already exists!".format(book.isbn))
                return

            self.books[book] = 1

    def isbn_already_exists(self, isbn):
        for book in self.books.keys():
            if(book.isbn is isbn):
                return True

        return False

    def add_user(self, name, email, user_books = None):
        # Check if user already exists
        if(self.users.keys().__contains__(email)):
            print("User with email: {} already exists!".format(email))
            return

        # Check that user has valid email
        if(self.validate_email(email) is False):
            print("User email: {} is not valid!".format(email))
            return

        self.users[email] = User(name, email)

        if(user_books is not None):
            for book in user_books:
                self.add_book_to_user(book, email)

    def validate_email(self, email):
        return email.__contains__("@") and (email.__contains__(".com") or email.__contains__(".edu") or email.__contains__(".org"))

    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def most_read_book(self):
        books_sorted = sorted(self.books, key = self.books.get)

        return books_sorted[0]

    def highest_rated_book(self):
        highest_rated_book = {}
        highest_rating = 0
        
        for book in self.books.keys():
            rating = book.get_average_rating()
            
            if(rating > highest_rating):
                highest_rated_book = book
                highest_rating = rating
        
        return highest_rated_book

    def most_positive_user(self):
        most_postive_user = {}
        highest_average_rating = 0

        for user in self.users.values():
            average_rating = user.get_average_rating()

            if(average_rating > highest_average_rating):
                most_postive_user = user
                highest_average_rating = average_rating

        return most_postive_user


# User classes
class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {} # book:rating

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("{}'s email has been updated".format(self.name))

    def read_book(self, book, rating = None):
        self.books[book] = rating

    def get_average_rating(self):
        # Filter unrated books away from average
        ratings_actual = [rating for rating in self.books.values() if rating is not None]
        ratings_sum = 0

        for rating in ratings_actual:
            ratings_sum += rating

        return ratings_sum / len(ratings_actual)

    def __repr__(self):
        return "User {}, email: {}, books read: {}".format(self.name, self.email, len(self.books))

    def __eq__(self, other_user):
        return self.name is other_user.name and self.email is other_user.email


# Book classes
class Book(object):
    ratings = []

    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, isbn):
        self.isbn = isbn
        print("ISBN of {} has been updated".format(self.title))

    def add_rating(self, rating):
        if(rating != None and 0 < rating < 5):
            self.ratings.append(rating)
        else:
            print("Invalid Rating")

    def get_average_rating(self):
        ratings_sum = 0
        
        for rating in self.ratings:
            ratings_sum += rating

        return ratings_sum / len(self.ratings)

    def __repr__(self):
        return "{}".format(self.title)

    def __eq__(self, other_book):
        return self.title is other_book.title and self.isbn is other_book.isbn

    def __hash__(self):
        return hash((self.title, self.isbn))

class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author
    
    def __repr__(self):
        return "{} by {}".format(self.title, self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{}, a {} manual on {}".format(self.title, self.level, self.subject)
