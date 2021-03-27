from model.contact import Contact


def test_delete_any_contact_from_list(app, db, check_ui):
    if len(db.get_contact_list()) == 0:
        contact = Contact().set_all_parameters_to_random_value()
        app.contact.create(contact)
    old_contacts = db.get_contact_list()

    # get id of randomly chosen contact
    removed_contact_id = app.contact.delete_any_contact_form_list()

    # expected list = old list without removed element
    expected_contact_list = list(filter(lambda c: c.id != removed_contact_id, old_contacts))

    new_contacts = db.get_contact_list()

    assert sorted(expected_contact_list) == sorted(new_contacts)
    if check_ui:
        assert sorted(new_contacts) == sorted(app.contact.get_contact_list())


def test_delete_any_contact_from_itself(app, db, check_ui):
    if len(db.get_contact_list()) == 0:
        contact = Contact().set_all_parameters_to_random_value()
        app.contact.create(contact)
    old_contacts = db.get_contact_list()

    # get id of randomly chosen contact
    removed_contact_id = app.contact.delete_any_contact_from_itself()

    # expected list = old list without removed element
    expected_contact_list = list(filter(lambda c: c.id != removed_contact_id, old_contacts))

    new_contacts = db.get_contact_list()

    assert sorted(expected_contact_list) == sorted(new_contacts)
    if check_ui:
        assert sorted(new_contacts) == sorted(app.contact.get_contact_list())
