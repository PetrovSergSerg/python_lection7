def test_add_group(app, json_groups):
    group = json_groups
    old_groups = app.group.get_group_list()
    app.group.create(group)

    # new list is longer, because we added 1 element
    assert app.group.count() == len(old_groups) + 1

    # if new list length is correct, then we can compare lists.
    # so we can get new list
    new_groups = app.group.get_group_list()

    # built expected list for equalizing NEW and EXPECTED
    # expected = old _list + new_group. And sort()
    # sort() will use method __lt__, which was overridden
    old_groups.append(group)
    assert sorted(new_groups) == sorted(old_groups)