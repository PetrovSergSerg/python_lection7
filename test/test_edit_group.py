from model.group import Group
import allure


def test_edit_any_group(app, db, check_ui):
    with allure.step(f'Given non-empty group list'):
        if len(db.get_group_list()) == 0:
            group = Group().set_all_parameters_to_random_value()
            app.group.create(group)
        old_groups = db.get_group_list()

    with allure.step(f'Given new state for group to edit'):
        group_new_state = Group().set_random_parameters_to_random_value()

    with allure.step(f'When edit random group to new state {group_new_state}'):
        # get id of randomly chosen group
        group_id = app.group.edit_any_group(group_new_state)

    with allure.step(f'Then group list count is not changed'):
        # check len of list was not changed
        assert app.group.count() == len(old_groups)

    with allure.step(f'Then new group list is equals to the old group list with 1 group changed'):
        # next(iterator, None) returns first group by condition or None if no element found
        # but we already got its id, so element exists! And we will not get None
        # so we can replace old group by new_state with new id is set
        edited_group = next((group for group in old_groups if group.id == group_id), None)
        index = old_groups.index(edited_group)
        group_new_state.id = group_id
        old_groups[index].update(group_new_state)

        # if new list length is correct, then we can compare lists.
        # so we can get new list
        new_groups = db.get_group_list()

        # check equalizing of sorted lists
        assert sorted(new_groups) == sorted(old_groups)
        if check_ui:
            assert sorted(new_groups) == sorted(app.group.get_group_list())
