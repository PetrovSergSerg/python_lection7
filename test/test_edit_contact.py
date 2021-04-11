from model.contact import Contact
import allure


def test_edit_any_contact_from_list_to_random_parameters(app, db, check_ui):
    with allure.step(f'Given non-empty contact list'):
        if len(db.get_contact_list()) == 0:
            contact = Contact().set_all_parameters_to_random_value()
            app.contact.create(contact)
        old_contacts = db.get_contact_list()

    with allure.step(f'Given new state for contact to edit'):
        contact_new_state = Contact().set_random_parameters_to_random_value()

    with allure.step(f'When edit random contact to new state {contact_new_state}'):
        contact_id = app.contact.edit_any_contact(contact_new_state)

    with allure.step(f'Then new contact list is equals to the old contact list with 1 contact changed'):
        # next(iterator, None) returns first group by condition or None if no element found
        # but we already got its id, so element exists! And we will not get None
        # so we can replace old group by new_state with new id is set
        edited_contact = next((c for c in old_contacts if c.id == contact_id), None)
        index = old_contacts.index(edited_contact)
        contact_new_state.id = contact_id
        old_contacts[index].update(contact_new_state)

        new_contacts = db.get_contact_list()

        assert sorted(new_contacts) == sorted(old_contacts)
        if check_ui:
            assert sorted(new_contacts) == sorted(app.contact.get_contact_list())


def test_edit_any_contact_from_list_to_handled_parameters(app, db, check_ui):
    with allure.step(f'Given non-empty contact list'):
        if len(db.get_contact_list()) == 0:
            contact = Contact().set_all_parameters_to_random_value()
            app.contact.create(contact)
        old_contacts = db.get_contact_list()

    with allure.step(f'Given new state for contact to edit'):
        contact_new_state = Contact(lastname='lastname', firstname='bbb', middlename='ccc', nickname='ddd', title='kkk',
                                    company='lll', address='mmm', phone_home='111', mobile='222', phone_work='333',
                                    fax='444', email_main='a@a.ru', email_secondary='b@b.ru', email_other='c@c.ru',
                                    homepage='http://', byear='1994', bmonth='April', bday='15', ayear='2003',
                                    amonth='September', aday='4', address_secondary='xxx', phone_secondary='777',
                                    notes='zzz')

    with allure.step(f'When edit random contact to new state {contact_new_state}'):
        contact_id = app.contact.edit_any_contact(contact_new_state)

    with allure.step(f'Then new contact list is equals to the old contact list with 1 contact changed'):
        # next(iterator, None) returns first group by condition or None if no element found
        # but we already got its id, so element exists! And we will not get None
        # so we can replace old group by new_state with new id is set
        edited_contact = next((c for c in old_contacts if c.id == contact_id), None)
        index = old_contacts.index(edited_contact)
        contact_new_state.id = contact_id
        old_contacts[index].update(contact_new_state)

        new_contacts = db.get_contact_list()

        assert sorted(new_contacts) == sorted(old_contacts)
        if check_ui:
            assert sorted(new_contacts) == sorted(app.contact.get_contact_list())
