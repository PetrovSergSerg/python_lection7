import pytest
from data.groups import testdata


@pytest.mark.parametrize("group", testdata, ids=[repr(g) for g in testdata])
def test_add_group(app, db, group, check_ui):
    old_groups = db.get_group_list()
    app.group.create(group)

    new_groups = db.get_group_list()

    old_groups.append(group)
    assert sorted(new_groups) == sorted(old_groups)
    if check_ui:
        assert sorted(new_groups) == sorted(app.group.get_group_list())