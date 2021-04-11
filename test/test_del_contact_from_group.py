from model.group import Group
from model.contact import Contact
from random import randint, sample
import allure


def test_delete_contacts_from_group(app, orm, check_ui):
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

    with allure.step(f'Given contact list and 1 group which are not in bind'):
        # get one random group which has contact list in bind
        (group, old_contact_list) = orm.get_random_group_and_contacts_in_bind()
        # if no group has contact create bind!
        if len(old_contact_list) == 0:
            # first of all get all contacts
            full_contact_list = orm.get_contact_list()
            # get sublist of random length from all contact_list
            old_contact_list = sample(full_contact_list, randint(1, len(full_contact_list)))
            # get 1 random group from group_list
            group = sample(orm.get_group_list(), 1)[0]
            # create bind
            app.contact.bind_contacts_to_group(old_contact_list, group)

    with allure.step(f'When unbind 1 contact of sublist from that group'):
        # get id of randomly chosen contact
        removed_contact_id = app.contact.delete_any_contact_from_group(group)

    with allure.step(f'Then expected contact list in bind to than group equals to '
                            f'old sublist without chosen contact'):
        # expected list = old list without removed element
        expected_contact_list = list(filter(lambda c: c.id != removed_contact_id, old_contact_list))
        new_contact_list = orm.get_contacts_in_group(group)

        assert sorted(expected_contact_list) == sorted(new_contact_list)
        if check_ui:
            assert sorted(new_contact_list) == sorted(app.contact.get_contact_list_in_group(group))
