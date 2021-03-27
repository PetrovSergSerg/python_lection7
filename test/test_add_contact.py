import pytest
from data.contacts import testdata


@pytest.mark.parametrize("contact", testdata, ids=[repr(c) for c in testdata])
def test_add_contact(app, db, contact, check_ui):
    old_contacts = db.get_contact_list()
    app.contact.create(contact)

    new_contacts = db.get_contact_list()

    old_contacts.append(contact)
    assert sorted(new_contacts) == sorted(old_contacts)
    if check_ui:
        assert sorted(new_contacts) == sorted(app.contact.get_contact_list())
