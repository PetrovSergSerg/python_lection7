from model.group import Group
import allure


def test_delete_any_group(app, db, check_ui):
    with allure.step(f'Given non-empty group list'):
        if len(db.get_group_list()) == 0:
            group = Group().set_all_parameters_to_random_value()
            app.group.create(group)
        old_groups = db.get_group_list()

    with allure.step(f'When delete random group from list'):
        # get id of randomly chosen group
        removed_group_id = app.group.delete_any_group()

    with allure.step(f'Then expected group list equals to new group list without deleted group'):
        # expected list = old list without removed element
        expected_group_list = list(filter(lambda g: g.id != removed_group_id, old_groups))
        new_groups = db.get_group_list()
        assert sorted(expected_group_list) == sorted(new_groups)
        if check_ui:
            assert sorted(new_groups) == sorted(app.group.get_group_list())
