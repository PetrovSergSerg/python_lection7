from model.contact import Contact


def test_edit_any_contact_from_list_to_random_parameters(app):
    if app.contact.count() == 0:
        contact = Contact().set_all_parameters_to_random_value()
        app.contact.create(contact)
    old_contacts = app.contact.get_contact_list()
    contact_new_state = Contact().set_random_parameters_to_random_value()
    (index, contact_old_state) = app.contact.edit_any_contact(contact_new_state)

    # next(iterator, None) returns first contact by condition or None if no element found
    # but we already got its id, so element exists! And we will not get None
    # so we can update old contact by new_state
    old_contacts[index] = contact_old_state
    old_contacts[index].update(contact_new_state)

    # check len of list was not changed
    assert app.contact.count() == len(old_contacts)

    # if new list length is correct, then we can compare lists.
    # so we can get new list
    new_contacts = app.contact.get_contact_list()

    # check equalizing of sorted lists
    assert sorted(new_contacts) == sorted(old_contacts)


def test_edit_any_contact_from_list_to_handled_parameters(app):
    if app.contact.count() == 0:
        contact = Contact().set_all_parameters_to_random_value()
        app.contact.create(contact)
    old_contacts = app.contact.get_contact_list()
    contact_new_state = Contact(lastname='lastname', firstname='bbb', middlename='ccc', nickname='ddd', title='kkk',
                                company='lll', address='mmm', phone_home='111', mobile='222', phone_work='333',
                                fax='444', email_main='a@a.ru', email_secondary='b@b.ru', email_other='c@c.ru',
                                homepage='http://', byear='1994', bmonth='April', bday='15', ayear='2003',
                                amonth='September', aday='4', address_secondary='xxx', phone_secondary='777',
                                notes='zzz')
    (index, contact_old_state) = app.contact.edit_any_contact(contact_new_state)

    # next(iterator, None) returns first contact by condition or None if no element found
    # but we already got its id, so element exists! And we will not get None
    # so we can update old contact by new_state
    old_contacts[index] = contact_old_state
    old_contacts[index].update(contact_new_state)

    # check len of list was not changed
    assert app.contact.count() == len(old_contacts)

    # if new list length is correct, then we can compare lists.
    # so we can get new list
    new_contacts = app.contact.get_contact_list()

    # check equalizing of sorted lists
    assert sorted(new_contacts) == sorted(old_contacts)
