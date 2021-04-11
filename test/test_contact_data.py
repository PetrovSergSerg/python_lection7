from random import randint
from model.contact import Contact
import allure


def test_contact_on_home_page(app):
    with allure.step(f'Given non-empty contact list from HOME PAGE'):
        if app.contact.count() == 0:
            contact = Contact().set_all_parameters_to_random_value()
            app.contact.create(contact)
        contact_list = app.contact.get_contact_list()

    with allure.step(f'Given random contact from HOME PAGE'):
        index = randint(0, len(contact_list) - 1)
        contact_from_home_page = contact_list[index]
    with allure.step(f'Given THAT contact from EDIT PAGE'):
        contact_from_edit_page = app.contact.get_contact_from_edit_page(index)

    with allure.step(f'Then contact from HOME PAGE equals to its data from EDIT PAGE'):
        assert contact_from_edit_page == contact_from_home_page
