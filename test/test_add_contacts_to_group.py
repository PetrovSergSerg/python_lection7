from model.group import Group
from model.contact import Contact
from random import randint, sample


def test_add_contacts_to_group(app, orm, check_ui):
    if len(orm.get_group_list()) == 0:
        count = randint(1, 10)
        for i in range(count):
            app.group.create(Group().set_all_parameters_to_random_value())

    if len(orm.get_contact_list()) == 0:
        count = randint(1, 10)
        for i in range(count):
            app.contact.create(Contact().set_all_parameters_to_random_value())

    (group, contact_list_from_db) = orm.get_random_group_and_contacts_not_in_bind()

    assert len(contact_list_from_db) > 0, 'All contacts in all groups'

    old_contact_list = orm.get_contacts_in_group(group)
    contact_sublist = sample(contact_list_from_db, randint(1, len(contact_list_from_db)))

    app.contact.bind_contacts_to_group(contact_sublist, group)

    expected_contact_list = old_contact_list + contact_sublist
    new_contact_list = orm.get_contacts_in_group(group)

    assert sorted(expected_contact_list) == sorted(new_contact_list)
    if check_ui:
        assert sorted(new_contact_list) == sorted(app.contact.get_contact_list_in_group(group))
