import pytest
import allure
from data.groups import testdata


@pytest.mark.parametrize("group", testdata, ids=[repr(g) for g in testdata])
def test_add_group(app, db, group, check_ui):
    with allure.step('Given a group list'):
        old_groups = db.get_group_list()

    with allure.step(f'When I add a group {group} to the list'):
        app.group.create(group)

    with allure.step(f'Then the new group list equals to the old list with the added group'):
        new_groups = db.get_group_list()
        old_groups.append(group)
        assert sorted(new_groups) == sorted(old_groups)
        if check_ui:
            assert sorted(new_groups) == sorted(app.group.get_group_list())