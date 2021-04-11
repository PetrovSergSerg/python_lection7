from model.group import Group
from model.contact import Contact
from random import randint, sample
import allure


def test_add_contacts_to_group(app, orm, check_ui):
    with allure.step(f'Given non-empty group list'):
        if len(orm.get_group_list()) == 0:
            count = randint(1, 10)
            for i in range(count):
                app.group.create(Group().set_all_parameters_to_random_value())

    with allure.step(f'Given non-empty contact list'):
        if len(orm.get_contact_list()) == 0:
            count = randint(1, 10)
            for i in range(count):
                app.contact.create(Contact().set_all_parameters_to_random_value())
        # Add 1 new contact for guarantee existing at least 1 contact and 1 group not in bind
        app.contact.create(Contact().set_all_parameters_to_random_value())

    with allure.step(f'Given contact list and 1 group which are not in bind'):
        # get random group and contact_list which are not in bind
        (group, contact_list_from_db) = orm.get_random_group_and_contacts_not_in_bind()

    with allure.step(f'When bind contact sublist and that group'):
        # get all contacts in chosen group (it may be empty, may be not)
        old_contact_list = orm.get_contacts_in_group(group)
        # get sublist of all contacts which are not in chosen group for adding to it
        contact_sublist = sample(contact_list_from_db, randint(1, len(contact_list_from_db)))
        # binding sublist to group
        app.contact.bind_contacts_to_group(contact_sublist, group)

    with allure.step(f'Then all contacts from sublist are in bind with group'):
        # build expected list = old_list which was in bind to group
        # + new sublist from all contacts which was not in bind
        expected_contact_list = old_contact_list + contact_sublist
        new_contact_list = orm.get_contacts_in_group(group)

        assert sorted(expected_contact_list) == sorted(new_contact_list)
        if check_ui:
            assert sorted(new_contact_list) == sorted(app.contact.get_contact_list_in_group(group))
