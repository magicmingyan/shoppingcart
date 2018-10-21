"""Customers at Hackbright."""


class Customer(object):
    """Ubermelon customer."""

    # TODO: need to implement this
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hashed_password = hash(password)

    def __repr__(self):
        """convenience"""

        return "<Customer: {}, {}, {}, {}>".format(self.first_name, self.last_name, self.email, self.password)


def read_file(filename):
    """read file"""
    customer_dict = {}
    file = open(filename,"r")
    for line in file:
        first_name, last_name, email, password = line.rstrip().split("|")
        customer_dict[email] = Customer(first_name, last_name, email, password)
    return customer_dict

def get_by_email(email):
    return customers[email]


customers = read_file("customers.txt")
