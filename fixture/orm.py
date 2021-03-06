from pony.orm import *
from datetime import datetime
from model.group import Group
from model.contact import Contact
# from pymysql.converters import decoders
from random import shuffle


class ORMFixture:
    db = Database()

    class ORMGroup(db.Entity):
        _table_ = 'group_list'
        id = PrimaryKey(int, column='group_id')
        name = Optional(str, column='group_name')
        header = Optional(str, column='group_header')
        footer = Optional(str, column='group_footer')
        contacts = Set(lambda: ORMFixture.ORMContact,
                       table='address_in_groups', column='id', reverse='groups', lazy=True)

    class ORMContact(db.Entity):
        _table_ = 'addressbook'
        id = PrimaryKey(int, column='id')
        firstname = Optional(str, column='firstname')
        lastname = Optional(str, column='lastname')
        address = Optional(str, column='address')
        email_main = Optional(str, column='email')
        email_secondary = Optional(str, column='email2')
        email_other = Optional(str, column='email3')
        phone_work = Optional(str, column='work')
        phone_home = Optional(str, column='home')
        phone_secondary = Optional(str, column='phone2')
        mobile = Optional(str, column='mobile')
        deprecated = Optional(datetime, column='deprecated')
        groups = Set(lambda: ORMFixture.ORMGroup,
                     table='address_in_groups', column='group_id', reverse='contacts', lazy=True)

    def __init__(self, host, name, user, password):
        self.db.bind('mysql', host=host, database=name, user=user, password=password)
        self.db.generate_mapping()
        sql_debug(True)

    def convert_groups_to_model(self, groups):
        def convert(g: Group):
            return Group(id=str(g.id), name=g.name, header=g.header, footer=g.footer)
        return list(map(convert, groups))

    def convert_contacts_to_model(self, contacts):
        def convert(c: Contact):
            return Contact(id=str(c.id), firstname=c.firstname, lastname=c.lastname, address=c.address,
                           email_main=c.email_main, email_secondary=c.email_secondary, email_other=c.email_other,
                           phone_work=c.phone_work, phone_home=c.phone_home, phone_secondary=c.phone_secondary,
                           mobile=c.mobile
                           )
        return list(map(convert, contacts))

    @db_session
    def get_group_list(self):
        return self.convert_groups_to_model(select(g for g in ORMFixture.ORMGroup))

    @db_session
    def get_contact_list(self):
        return self.convert_contacts_to_model(select(c for c in ORMFixture.ORMContact if c.deprecated is None))

    @db_session
    def get_contacts_in_group(self, group):
        orm_group = list(select(g for g in ORMFixture.ORMGroup if g.id == group.id))[0]
        return self.convert_contacts_to_model(orm_group.contacts)

    @db_session
    def get_contacts_not_in_group(self, group):
        orm_group = list(select(g for g in ORMFixture.ORMGroup if g.id == group.id))[0]
        orm_contacts = select(c for c in ORMFixture.ORMContact
                                   if c.deprecated is None and
                                   orm_group not in c.groups)
        return self.convert_contacts_to_model(orm_contacts)

    def get_random_group_and_contacts_not_in_bind(self):
        group = Group()
        contact_list = []
        group_list = self.get_group_list()
        shuffle(group_list)

        for g in group_list:
            contact_list = self.get_contacts_not_in_group(g)
            if len(contact_list) > 0:
                group = g
                break

        return group, contact_list

    def get_random_group_and_contacts_in_bind(self):
        group = Group()
        contact_list = []
        group_list = self.get_group_list()
        shuffle(group_list)

        for g in group_list:
            contact_list = self.get_contacts_in_group(g)
            if len(contact_list) > 0:
                group = g
                break

        return group, contact_list