from random import randint, getrandbits, choice
import model.utils as utils
import datetime
import data.constants as c


class Contact:
    def __init__(self, id=None, lastname=None, firstname=None, middlename=None, nickname=None,
                 title=None, company=None, address=None, phone_home=None, mobile=None, phone_work=None, fax=None,
                 email_main=None, email_secondary=None, email_other=None, homepage=None,
                 byear=None, bmonth=None, bday=None, ayear=None, amonth=None, aday=None,
                 address_secondary=None, phone_secondary=None, notes=None, emails=None, phones=None):
        self.id = id
        self.lastname = lastname
        self.firstname = firstname
        self.middlename = middlename
        self.nickname = nickname
        self.title = title
        self.company = company
        self.address = address
        self.phone_home = phone_home
        self.mobile = mobile
        self.phone_work = phone_work
        self.fax = fax
        self.email_main = email_main
        self.email_secondary = email_secondary
        self.email_other = email_other
        self.homepage = homepage
        self.byear = byear
        self.bmonth = bmonth
        self.bday = bday
        self.ayear = ayear
        self.amonth = amonth
        self.aday = aday
        self.address_secondary = address_secondary
        self.phone_secondary = phone_secondary
        self.notes = notes
        self.emails = emails if emails is not None else self.calculate_emails()
        self.phones = phones if phones is not None else self.calculate_phones()

    def calculate_emails(self):
        # get list of emails for field in contact_list
        emails = [self.email_main, self.email_secondary, self.email_other]
        # filter this list by extracting all not-None elements
        emails = list(filter(lambda x: x is not None and x != "", emails))
        # and get string of list splitting all elements by "\n"
        return "" if len(emails) == 0 else "\n".join(emails)

    def calculate_phones(self):
        # get list of phones for field in contact_list
        phones = [self.phone_home, self.mobile, self.phone_work, self.phone_secondary]

        # filter this list by extracting all not-None elements
        phones = list(map(lambda x: utils.clear(x), (filter(lambda x: x is not None and x != "", phones))))

        # and get string of list splitting all elements by "\n"
        return utils.clear("" if len(phones) == 0 else "\n".join(phones))

    def set_empty_parameters(self):
        for name, value in self.__dict__.items():
            if name in ['bday', 'bmonth', 'aday', 'amonth']:
                setattr(self, name, '-')
            else:
                setattr(self, name, '')
        self.id = None

        return self

    def set_random_parameters_to_random_value(self):
        # getrandbits(1) returns 0 or 1 with 50% probability
        # with 50% probability generate random word on alphabet with random length
        # and with probability 50% returns EMPTY_STRING
        if bool(getrandbits(1)):
            self.lastname = '' if bool(getrandbits(1)) else utils.get_random_word(c.ALPHABET, randint(3, 10))
        if bool(getrandbits(1)):
            self.firstname = '' if bool(getrandbits(1)) else utils.get_random_word(c.ALPHABET, randint(3, 10))
        if bool(getrandbits(1)):
            self.middlename = '' if bool(getrandbits(1)) else utils.get_random_word(c.ALPHABET, randint(3, 10))
        if bool(getrandbits(1)):
            self.nickname = '' if bool(getrandbits(1)) else utils.get_random_word(c.ALPHABET, randint(3, 10))

        # getrandbits(1) returns 0 or 1 with 50% probability
        # with 50% probability generate random word on alphabet with random length
        # and with probability 50% returns EMPTY_STRING
        if bool(getrandbits(1)):
            self.title = '' if bool(getrandbits(1)) else utils.get_random_word(c.ALPHABET, randint(3, 10))
        if bool(getrandbits(1)):
            self.company = '' if bool(getrandbits(1)) else utils.get_random_word(c.ALPHABET, randint(3, 10))
        if bool(getrandbits(1)):
            self.address = '' if bool(getrandbits(1)) else utils.get_random_word(c.ALPHABET + ' ', randint(10, 20))

        # 30% probability to be empty value
        if bool(getrandbits(1)):
            self.phone_home = '' if randint(0, 2) < 1 else choice(c.CITY_PHONE_TEMPLATES).get_value()
        # 10% probability to be empty value
        if bool(getrandbits(1)):
            self.mobile = '' if randint(0, 9) < 1 else choice(c.MOBILE_PHONE_TEMPLATES).get_value()
        # 50% probability to be empty value
        if bool(getrandbits(1)):
            self.phone_work = '' if bool(getrandbits(1)) else choice(c.CITY_PHONE_TEMPLATES).get_value()
        # 10% probability to be empty value
        if bool(getrandbits(1)):
            self.fax = '' if randint(0, 9) < 1 else choice(c.CITY_PHONE_TEMPLATES).get_value()

        # randint(0, 4) < 1 = 20%; randint(0, 4) < 4 = 80%
        # with some probability generate random word on alphabet with random length
        if bool(getrandbits(1)):
            self.email_main = '' if randint(0, 4) < 1 else utils.get_random_email(c.ALPHABET)
        if bool(getrandbits(1)):
            self.email_secondary = '' if randint(0, 4) < 4 else utils.get_random_email(c.ALPHABET)
        if bool(getrandbits(1)):
            self.email_other = '' if randint(0, 4) < 4 else utils.get_random_email(c.ALPHABET)
        if bool(getrandbits(1)):
            self.homepage = '' if bool(getrandbits(1)) \
                else 'http://' + utils.get_random_word(c.ALPHABET, randint(3, 10)) + '.com'

        start = datetime.date(1980, 1, 1)
        end = datetime.date(2000, 12, 31)
        bd = utils.get_random_date(start, end)  # get random date between given dates
        if bool(getrandbits(1)):  # 50% probability set birthdate
            self.byear = bd.strftime('%Y')  # get year from this date
            self.bmonth = bd.strftime('%B')  # get month in format April, January, ...
            self.bday = str(int(bd.strftime('%d')))  # because %d is date with leading 0: 01, 02, 03, ... 11, 12, ...

        if bool(getrandbits(1)):  # 50% probability to generate anniversary date
            anniversary = utils.get_random_date(bd, datetime.date.today())  # random date from BD to TODAY
            self.ayear = anniversary.strftime('%Y')
            self.amonth = anniversary.strftime('%B')
            self.aday = str(int(anniversary.strftime('%d')))

        # randint(0, 2) < 2 = 66%; getrandbits(1) returns 0 or 1 with 50% probability
        # with some probability generate random word on alphabet with random length
        if bool(getrandbits(1)):
            self.address_secondary = '' if randint(0, 2) < 2 else utils.get_random_word(c.ALPHABET + ' ',
                                                                                        randint(10, 20))
        if bool(getrandbits(1)):
            self.phone_secondary = '' if randint(0, 2) < 2 else choice(c.CITY_PHONE_TEMPLATES).get_value()
        if bool(getrandbits(1)):
            self.notes = '' if bool(getrandbits(1)) else utils.get_random_word(c.ALPHABET + ' ', randint(10, 20))
        self.emails = self.calculate_emails()
        self.phones = self.calculate_phones()

        return self

    def set_all_parameters_to_random_value(self):
        self.lastname = utils.get_random_word(c.ALPHABET, randint(3, 10))
        self.firstname = utils.get_random_word(c.ALPHABET, randint(3, 10))
        self.middlename = utils.get_random_word(c.ALPHABET, randint(3, 10))
        self.nickname = utils.get_random_word(c.ALPHABET, randint(3, 10))

        self.title = utils.get_random_word(c.ALPHABET, randint(3, 10))
        self.company = utils.get_random_word(c.ALPHABET, randint(3, 10))
        self.address = utils.get_random_word(c.ALPHABET + ' ', randint(10, 20))

        self.phone_home = choice(c.CITY_PHONE_TEMPLATES).get_value()
        self.mobile = choice(c.MOBILE_PHONE_TEMPLATES).get_value()
        self.phone_work = choice(c.CITY_PHONE_TEMPLATES).get_value()
        self.fax = choice(c.CITY_PHONE_TEMPLATES).get_value()

        self.email_main = utils.get_random_email(c.ALPHABET)
        self.email_secondary = utils.get_random_email(c.ALPHABET)
        self.email_other = utils.get_random_email(c.ALPHABET)
        self.homepage = 'http://' + utils.get_random_word(c.ALPHABET, randint(3, 10)) + '.com'

        start = datetime.date(1980, 1, 1)
        end = datetime.date(2000, 12, 31)
        bd = utils.get_random_date(start, end)  # get random date between given dates
        self.byear = bd.strftime('%Y')  # get year from this date
        self.bmonth = bd.strftime('%B')  # get month in format April, January, ...
        self.bday = str(int(bd.strftime('%d')))  # because %d is date with leading 0: 01, 02, 03, ... 11, 12, ...

        anniversary = utils.get_random_date(bd, datetime.date.today())  # random date from BD to TODAY
        self.ayear = anniversary.strftime('%Y')
        self.amonth = anniversary.strftime('%B')
        self.aday = str(int(anniversary.strftime('%d')))

        self.address_secondary = '' if randint(0, 2) < 2 else utils.get_random_word(c.ALPHABET + ' ', randint(10, 20))
        self.phone_secondary = '' if randint(0, 2) < 2 \
            else choice(c.MOBILE_PHONE_TEMPLATES + c.CITY_PHONE_TEMPLATES).get_value()
        self.notes = '' if bool(getrandbits(1)) else utils.get_random_word(c.ALPHABET + ' ', randint(10, 20))

        self.emails = self.calculate_emails()
        self.phones = self.calculate_phones()

        return self

    def update(self, to):
        if to.lastname is not None:
            self.lastname = to.lastname
        if to.firstname is not None:
            self.firstname = to.firstname
        if to.middlename is not None:
            self.middlename = to.middlename
        if to.nickname is not None:
            self.nickname = to.nickname
        if to.title is not None:
            self.title = to.title
        if to.company is not None:
            self.company = to.company
        if to.address is not None:
            self.address = to.address
        if to.phone_home is not None:
            self.phone_home = to.phone_home
        if to.mobile is not None:
            self.mobile = to.mobile
        if to.phone_work is not None:
            self.phone_work = to.phone_work
        if to.fax is not None:
            self.fax = to.fax
        if to.email_main is not None:
            self.email_main = to.email_main
        if to.email_secondary is not None:
            self.email_secondary = to.email_secondary
        if to.email_other is not None:
            self.email_other = to.email_other
        if to.homepage is not None:
            self.homepage = to.homepage
        if to.byear is not None:
            self.byear = to.byear
        if to.bmonth is not None:
            self.bmonth = to.bmonth
        if to.bday is not None:
            self.bday = to.bday
        if to.ayear is not None:
            self.ayear = to.ayear
        if to.amonth is not None:
            self.amonth = to.amonth
        if to.aday is not None:
            self.aday = to.aday
        if to.address_secondary is not None:
            self.address_secondary = to.address_secondary
        if to.phone_secondary is not None:
            self.phone_secondary = to.phone_secondary
        if to.notes is not None:
            self.notes = to.notes
        self.emails = self.calculate_emails()
        self.phones = self.calculate_phones()

    def __eq__(self, other):
        return (self.id is None
                or other.id is None
                or self.id == other.id) \
               and utils.xstr(self.lastname) == utils.xstr(other.lastname) \
               and utils.xstr(self.firstname) == utils.xstr(other.firstname) \
               and ' '.join(utils.xstr(self.address).strip().split()) == ' '.join(utils.xstr(other.address).strip().split()) \
               and self.emails == other.emails \
               and self.phones == other.phones

    def __repr__(self):
        fio = [self.lastname, self.firstname]
        return f'Contact({"id="+self.id+", " if self.id is not None else ""}' \
               f'FIO="{" ".join(filter(lambda x: x is not None and x != "", fio))}", ' \
               f'ADDRESS="{self.address}"'

    def __lt__(self, other):
        # None >> any integer
        # self.id = None => return False (left bigger)
        # other.id is None => return True (right is bigger)
        # else compare int(self.id) <> int(other.id), because type(Group.id) = str, but it's a number!
        return self.id is not None \
               and (other.id is None
                    or int(self.id) < int(other.id))
