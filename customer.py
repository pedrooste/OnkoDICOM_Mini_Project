"""Customer object used for sqlite demo"""


class Customer:
    """Example Customer object"""

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay

    @property
    def email(self):
        """Gets users email and formats"""
        return '{}.{}@email.com'.format(self.first, self.last)

    @property
    def fullname(self):
        """gets users full name"""
        return '{} {}'.format(self.first, self.last)

    def __repr__(self):
        return 'Customer({}, {}, {})'.format(self.first, self.last, self.pay)
