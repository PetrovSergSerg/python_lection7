import model.utils as utils
from random import randint, getrandbits
import data.constants as c


class Group:
    def __init__(self, id=None, name=None, header=None, footer=None):
        self.id = id
        self.name = name
        self.header = header
        self.footer = footer

    def set_empty_parameters(self):
        for name, value in self.__dict__.items():
            setattr(self, name, '')
        self.id = None
        return self

    def set_random_parameters_to_random_value(self):
        if bool(getrandbits(1)):
            self.name = '' if randint(0, 4) < 1 else utils.get_random_word(c.ALPHABET, randint(3, 10))
        if bool(getrandbits(1)):
            self.header = '' if randint(0, 4) < 1 else utils.get_random_word(c.ALPHABET + ' '*5, randint(10, 20))
        if bool(getrandbits(1)):
            self.footer = '' if randint(0, 4) < 1 else utils.get_random_word(c.ALPHABET + ' '*5, randint(10, 20))
        return self

    def set_all_parameters_to_random_value(self):
        self.name = utils.get_random_word(c.ALPHABET, randint(3, 10))
        self.header = utils.get_random_word(c.ALPHABET + ' '*5, randint(10, 20))
        self.footer = utils.get_random_word(c.ALPHABET + ' '*5, randint(10, 20))
        return self

    def __eq__(self, other):
        return (self.id is None
                or other.id is None
                or self.id == other.id) \
               and self.name == other.name

    def __repr__(self):
        return f'Group({"id="+self.id+", " if self.id is not None else ""}' \
               f'name="{self.name}", header="{self.header}", footer="{self.footer}")'

    def __lt__(self, other):
        # None >> any integer
        # self.id = None => return False (left bigger)
        # other.id is None => return True (right is bigger)
        # else compare int(self.id) <> int(other.id), because type(Group.id) = str, but it's a number!
        return self.id is not None \
               and (other.id is None
                    or int(self.id) < int(other.id))
