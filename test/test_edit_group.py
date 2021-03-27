from model.group import Group


def test_edit_any_group(app, db, check_ui):
    if len(db.get_group_list()) == 0:
        group = Group().set_all_parameters_to_random_value()
        app.group.create(group)
    old_groups = db.get_group_list()

    group_new_state = Group().set_random_parameters_to_random_value()

    # get id of randomly chosen group
    group_id = app.group.edit_any_group(group_new_state)

    # check len of list was not changed
    assert app.group.count() == len(old_groups)

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
