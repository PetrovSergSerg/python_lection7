from random import randint
from model.contact import Contact


def test_contact_on_home_page(app):
    if app.contact.count() == 0:
        contact = Contact().set_all_parameters_to_random_value()
        app.contact.create(contact)
    contact_list = app.contact.get_contact_list()
    index = randint(0, len(contact_list) - 1)
    contact_from_home_page = contact_list[index]
    contact_from_edit_page = app.contact.get_contact_from_edit_page(index)
    assert contact_from_edit_page == contact_from_home_page
