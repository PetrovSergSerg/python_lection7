from model.contact import Contact
import allure


def test_delete_any_contact_from_list(app, db, check_ui):
    with allure.step(f'Given non-empty contact list'):
        if len(db.get_contact_list()) == 0:
            contact = Contact().set_all_parameters_to_random_value()
            app.contact.create(contact)
        old_contacts = db.get_contact_list()

    with allure.step(f'When delete random contact from list'):
        # get id of randomly chosen contact
        removed_contact_id = app.contact.delete_any_contact_from_list()

    with allure.step(f'Then expected contact list equals to new contact list without deleted contact'):
        # expected list = old list without removed element
        expected_contact_list = list(filter(lambda c: c.id != removed_contact_id, old_contacts))
        new_contacts = db.get_contact_list()
        assert sorted(expected_contact_list) == sorted(new_contacts)
        if check_ui:
            assert sorted(new_contacts) == sorted(app.contact.get_contact_list())


def test_delete_any_contact_from_itself(app, db, check_ui):
    with allure.step(f'Given non-empty contact list'):
        if len(db.get_contact_list()) == 0:
            contact = Contact().set_all_parameters_to_random_value()
            app.contact.create(contact)
        old_contacts = db.get_contact_list()

    with allure.step(f'When delete random contact from itself'):
        # get id of randomly chosen contact
        removed_contact_id = app.contact.delete_any_contact_from_itself()

    with allure.step(f'Then expected contact list equals to new contact list'):
        # expected list = old list without removed element
        expected_contact_list = list(filter(lambda c: c.id != removed_contact_id, old_contacts))
        new_contacts = db.get_contact_list()
        assert sorted(expected_contact_list) == sorted(new_contacts)
        if check_ui:
            assert sorted(new_contacts) == sorted(app.contact.get_contact_list())
