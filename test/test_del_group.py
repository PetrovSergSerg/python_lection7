from model.group import Group


def test_delete_any_group(app, db, check_ui):
    if len(db.get_group_list()) == 0:
        group = Group().set_all_parameters_to_random_value()
        app.group.create(group)
    old_groups = db.get_group_list()

    # get id of randomly chosen group
    removed_group_id = app.group.delete_any_group()

    # expected list = old list without removed element
    expected_group_list = list(filter(lambda g: g.id != removed_group_id, old_groups))

    new_groups = db.get_group_list()

    assert sorted(expected_group_list) == sorted(new_groups)
    if check_ui:
        assert sorted(new_groups) == sorted(app.group.get_group_list())
