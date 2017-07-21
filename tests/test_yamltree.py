# -*- coding: utf-8 -*-

import pytest

def test_yamltree_class(tmpdir):
    # at this point py.path.local should already be monkey-patched by conftest
    assert hasattr(tmpdir, 'yaml_check')

    # for now this is an empty directory - this check should pass
    assert tmpdir.yaml_check('{}')

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
    tmpdir.yaml_create(struct)

    # check individual parts
    assert tmpdir.join('data.txt').yaml_check('this is just a file')
    # and check that yaml really works
    assert tmpdir.join('data.txt').yaml_check('"this is just a file"')
    # also for empty dirs
    assert tmpdir.join('emptydir').yaml_check('{}')

    # check something "traditionally"
    assert tmpdir.join('Keys', 'f7').read() == 'Remove!'
    assert tmpdir.join('data.txt').read() == 'this is just a file'
    assert tmpdir.join('empty').read() == ''
    assert tmpdir.join('emptydir').isdir()
    assert tmpdir.join('emptydir').listdir() == []
    assert tmpdir.join('nested', 'subnested', 'hello').read() == 'world'

    # and finally check that it is accepted by yaml_check as well
    assert tmpdir.yaml_check(struct)

    # now we want to make sure that check doesn't allow extra files...
    tmpdir.join('something.txt').write('huh')
    with pytest.raises(AssertionError):
        tmpdir.yaml_check(struct)

    # ...that file contents are checked...
    tmpdir.join('something.txt').remove()
    tmpdir.join('data.txt').write('another data!!11')
    with pytest.raises(AssertionError):
        tmpdir.yaml_check(struct)

    # ...that missing files are not allowed...
    tmpdir.join('data.txt').remove()
    with pytest.raises(AssertionError):
        tmpdir.yaml_check(struct)

    # ...and that file is differentiated from directory.
    with pytest.raises(AssertionError):
        tmpdir.yaml_check('I thought it is a file')
    with pytest.raises(AssertionError):
        tmpdir.yaml_check('nested: I thought it is a file')
