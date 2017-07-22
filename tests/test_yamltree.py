# -*- coding: utf-8 -*-

import pytest

def test_yamltree_class(tmpdir):
    from pytest_yamltree import YamlTree

    tmp = tmpdir.strpath

    # for now this is an empty directory - this check should pass
    YamlTree(tmp, '{}')

    # let's create some data
    struct = r'''
        Keys:
            f1: help
            f2: open editor
            f7: Remove!
        data.txt: this is just a file
        empty: ''
        emptydir: {}
        nested:
            subnested:
                hello: world
    '''
    YamlTree(tmp, struct).create()

    # check individual parts
    assert YamlTree.check_from(
        tmpdir.join('data.txt').strpath,
        'this is just a file',
    )
    # and check that yaml really works
    assert YamlTree.check_from(
        tmpdir.join('data.txt').strpath,
        '"this is just a file"',
    )
    # also for empty dirs
    assert YamlTree.check_from(
        tmpdir.join('emptydir').strpath,
        '{}',
    )

    # check something "traditionally"
    assert tmpdir.join('Keys', 'f7').read() == 'Remove!'
    assert tmpdir.join('data.txt').read() == 'this is just a file'
    assert tmpdir.join('empty').read() == ''
    assert tmpdir.join('emptydir').isdir()
    assert tmpdir.join('emptydir').listdir() == []
    assert tmpdir.join('nested', 'subnested', 'hello').read() == 'world'

    # and finally check that it is accepted by yaml_check as well
    assert YamlTree.check_from(tmp, struct)

    # now we want to make sure that check doesn't allow extra files...
    tmpdir.join('something.txt').write('huh')
    with pytest.raises(AssertionError):
        YamlTree.check_from(tmp, struct)

    # ...that file contents are checked...
    tmpdir.join('something.txt').remove()
    tmpdir.join('data.txt').write('another data!!11')
    with pytest.raises(AssertionError):
        YamlTree.check_from(tmp, struct)

    # ...that missing files are not allowed...
    tmpdir.join('data.txt').remove()
    with pytest.raises(AssertionError):
        YamlTree.check_from(tmp, struct)

    # ...and that file is differentiated from directory.
    with pytest.raises(AssertionError):
        YamlTree.check_from(tmp, 'I thought it is a file')
    with pytest.raises(AssertionError):
        YamlTree.check_from(tmp, 'nested: I thought it is a file')
