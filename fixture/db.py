import mysql.connector
import contextlib
from model.group import Group
from model.contact import Contact


class DbFixture:
    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.connection = mysql.connector.connect(host=host,
                                                  database=name,
                                                  user=user,
                                                  password=password,
                                                  autocommit=True)

    @contextlib.contextmanager
    def get_cursor(self):
        cursor = self.connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def get_group_list(self):
        group_list = []
        with self.get_cursor() as cursor:
            cursor.execute("SELECT group_id, group_name, group_header, group_footer FROM group_list")
            for row in cursor:
                (id, name, header, footer) = row
                group_list.append(Group(id=str(id), name=name, header=header, footer=footer))
        return group_list

    def get_contact_list(self):
        contact_list = []
        with self.get_cursor() as cursor:
            cursor.execute("SELECT id, firstname, lastname, address, email, email2, email3, mobile, work, home, phone2 FROM addressbook WHERE deprecated = '0000-00-00 00:00:00'")
            for row in cursor:
                (id, firstname, lastname, address,
                 email, email2, email3,
                 mobile, work, home, phone2) = row
                contact_list.append(Contact(id=str(id), firstname=firstname, lastname=lastname, address=address,
                                            email_main=email, email_secondary=email2, email_other=email3,
                                            phone_work=work, phone_home=home, phone_secondary=phone2, mobile=mobile))
        return contact_list

    def destroy(self):
        self.connection.close()
