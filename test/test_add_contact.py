def test_add_contact(app, json_contacts):
    contact = json_contacts
    old_contacts = app.contact.get_contact_list()
    app.contact.create(contact)

    # new list is longer, because we added 1 element
    assert app.contact.count() == len(old_contacts) + 1

    # if new list length is correct, then we can compare lists.
    # so we can get new list
    new_contacts = app.contact.get_contact_list()

    # make sure that all elements of OLD list are in NEW list
    assert all(elem in new_contacts for elem in old_contacts)

    # built expected list for equalizing NEW and EXPECTED
    # expected list = old_list + new contact. And sort()
    # sort() will use method __lt__, which was overridden
    old_contacts.append(contact)
    assert sorted(new_contacts) == sorted(old_contacts)
