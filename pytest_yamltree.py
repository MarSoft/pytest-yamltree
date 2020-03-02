# -*- coding: utf-8 -*-
"""
Basic usage: we monkey-patch py.path.local object
to add yaml_create and yaml_check methods to it.
As a result, these methods are available on e.g. `tmpdir` fixture's object.
"""

import warnings

import py
import pytest
import yaml


DEFAULT = object()


class YamlTree(object):
    """
    Declare file&directory trees in yaml format.
    Each mapping (even empty) corresponds to a directory,
    and each string corresponds to file;
    other data types are not supported.

    Once declared, tree can be `create`d or `check`ed.
    When checking, real directory sturcture and files content
    is expected to be completely identical to the declaration.
    """
    def __init__(self, root, descr):
        self.root = py.path.local(root)
        self.data = yaml.safe_load(descr)

    def _walk(self, ondir, onleaf, root=DEFAULT, data=DEFAULT):
        if root is DEFAULT:
            root = self.root
        if data is DEFAULT:
            data = self.data

        if isinstance(data, dict):
            ondir(root, data)
            for k, v in data.items():
                sub = root.join(k)
                self._walk(ondir, onleaf, sub, v)
        else:
            onleaf(root, data)

    def create(self):
        self._walk(
            lambda d, data: d.ensure(dir=True),
            lambda f, data: f.write(data),
        )

    def check(self):
        def ondir(d, data):
            # for dirs, check that content names match -
            # no extra and no missing
            assert d.exists()
            assert d.isdir()
            assert set(l.basename for l in d.listdir()) == set(data.keys())

        def onfile(f, data):
            # for file, check contents
            assert f.exists()
            assert f.isfile()
            assert f.read() == data

        self._walk(ondir, onfile)
        return True  # to allow using as `assert yamltree.check()`

    @classmethod
    def create_from(cls, root, data):
        return cls(root, data).create()

    @classmethod
    def check_from(cls, root, data):
        return cls(root, data).check()


# just for easier access
@pytest.fixture
def yamltree():
    return YamlTree


def pytest_configure(config):
    # TODO allow disabling this somehow

    for attr in ('yaml_create', 'yaml_check'):
        if hasattr(py.path.local, attr):
            warnings.warn(
                'Looks like {attr} is already declared on py.path.local; '
                'skipping monkey-patching'.format(attr=attr))
            return

    # monkey-patch py.path.local to add support for YamlTree
    py.path.local.yaml_create = lambda self, desc: \
        YamlTree.create_from(self, desc)
    py.path.local.yaml_check = lambda self, desc: \
        YamlTree.check_from(self, desc)
