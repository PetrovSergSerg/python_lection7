import pytest
from data.contacts import testdata
import allure


@pytest.mark.parametrize("contact", testdata, ids=[repr(c) for c in testdata])
def test_add_contact(app, db, contact, check_ui):
    with allure.step('Given a contact list'):
        old_contacts = db.get_contact_list()

    with allure.step(f'When I add a contact {contact} to the list'):
        app.contact.create(contact)

    with allure.step(f'Then the new contact list equals to the old list with the added contact'):
        new_contacts = db.get_contact_list()

        old_contacts.append(contact)
        assert sorted(new_contacts) == sorted(old_contacts)
        if check_ui:
            assert sorted(new_contacts) == sorted(app.contact.get_contact_list())
