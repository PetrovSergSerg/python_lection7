from model.group import Group
from model.contact import Contact
import allure


def test_group_list(app, db):
    with allure.step('Given a group list from UI'):
        group_list_from_web = app.group.get_group_list()

    with allure.step('Given a group list from DB'):
        def clean(g: Group):
            return Group(id=g.id, name=g.name.strip(), header=g.header, footer=g.footer)
        group_list_from_db = list(map(clean, db.get_group_list()))

    with allure.step('Then group list from UI equals to group list from DB'):
        assert app.group.count() == len(group_list_from_db)
        assert sorted(group_list_from_web) == sorted(group_list_from_db)


def test_contact_list(app, db):
    with allure.step('Given a contact list from UI'):
        contact_list_from_web = app.contact.get_contact_list()

    with allure.step('Given a contact list from DB'):
        def clean(c: Contact):
            return Contact(id=c.id, lastname=c.lastname.strip(), firstname=c.firstname.strip(), address=c.address.strip(),
                           email_main=c.email_main, email_secondary=c.email_secondary, email_other=c.email_other,
                           mobile=c.mobile, phone_work=c.phone_work,
                           phone_home=c.phone_home, phone_secondary=c.phone_secondary)

        contact_list_from_db = list(map(clean, db.get_contact_list()))

    with allure.step('Then contact list from UI equals to contact list from DB'):
        assert app.contact.count() == len(contact_list_from_db)
        assert sorted(contact_list_from_web) == sorted(contact_list_from_db)
