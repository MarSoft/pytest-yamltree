===============
pytest-yamltree
===============

.. image:: https://travis-ci.org/MarSoft/pytest-yamltree.svg?branch=master
    :target: https://travis-ci.org/MarSoft/pytest-yamltree
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/MarSoft/pytest-yamltree?branch=master
    :target: https://ci.appveyor.com/project/MarSoft/pytest-yamltree/branch/master
    :alt: See Build Status on AppVeyor

Create or check file/directory trees described by YAML

----

This `Pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `Cookiecutter-pytest-plugin`_ template.


Features
--------

* Monkey-patches `py.path.local`_ class (the one behind `tmpdir`_ fixture) to append `yaml_create` and `yaml_check` methods for easy access.
* Use it like this::

    def test_foo(tmpdir):
        tmpdir.yaml_create("""
            directory_one:
                file1: Hello World
                file2: "Including\nLine\nBreaks\n"
                subdir:
                    file3: |
                        Some raw content here.
                        It is probably better readable.
            directory_two:
                arrow.gif: !!binary |
                    R0lGODlhDAAMAIQAAP//9/X17unp5WZmZgAAAOfn515eXvPz7Y6OjuDg4J+fn5
                    OTk6enp56enmlpaWNjY6Ojo4SEhP/++f/++f/++f/++f/++f/++f/++f/++f/+
                    +f/++f/++f/++f/++f/++SH+Dk1hZGUgd2l0aCBHSU1QACwAAAAADAAMAAAFLC
                    AgjoEwnuNAFOhpEMTRiggcz4BNJHrv/zCFcLiwMWYNG84BwwEeECcgggoBADs=
        """)

        # now these files are created under tmpdir
        assert tmpdir.join('directory_one', 'file1').read() == 'Hello World'

        # also can check that directory structure corresponds to the declaration
        tmpdir.yaml_check("""
            directory_one:
                file1: Content
            directory_two: {}  # empty mapping means empty directory
        """)


Requirements
------------

* PyYAML


Installation
------------

You can install "pytest-yamltree" via `pip`_ from `PyPI`_::

    $ pip install pytest-yamltree


Usage
-----

* TODO

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-yamltree" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/MarSoft/pytest-yamltree/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
.. _`py.path.local`: http://py.readthedocs.io/en/latest/path.html
.. _`tmpdir`: https://docs.pytest.org/en/latest/tmpdir.html
