Contributing
=========================

As an open source project, Mesa welcomes contributions of many forms.

In no particular order, examples include:

- Code patches
- Bug reports and patch reviews
- New features
- Documentation improvements
- Tutorials

No contribution is too small. Although, contributions can be too big, so let's discuss via the `email list`_ OR `an issue`_.

**To submit a contribution**

- Create a ticket for the item that you are working on.
- Fork the Mesa repository.
- Create a new branch if you aren't contributing to an existing branch.
- Edit the code.
- Use `PEP8`_ and the `Google Style Guide`_ as the coding standards for Python
- If implementing a new feature, include some documentation.
- Make sure that you contribution will pass Travis build by having flake8 come back with no errors and make sure test coverage has not decreased.

    - Install libraries to review: ``pip install flake8 nose``
    - To run flake8: ``flake8 . --ignore=F403,E501,E123,E128 --exclude=docs,build``
    - To see test coverage: ``nosetests --with-coverage --cover-package=mesa``
- Submit as a pull request.
- Describe the change w/ ticket number(s) that the code fixes.

.. _`email list` : https://groups.google.com/forum/#!forum/projectmesa
.. _`an issue` : https://github.com/projectmesa/mesa/issues
.. _`PEP8` : https://www.python.org/dev/peps/pep-0008
.. _`Google Style Guide` : https://google.github.io/styleguide/pyguide.html


Testing
--------

.. image:: https://coveralls.io/repos/projectmesa/mesa/badge.svg
    :target: https://coveralls.io/r/projectmesa/mesa

We are continually working to improve our testing. At the moment, we've been testing features by implementing them in simple models. This is useful since it also expands the library of sample models. We also have several traditional unit tests in the tests/ folder.

If you're changing previous Mesa features, please make sure of the following:

- Your changes pass the current tests.
- Your changes don't break the models or your changes include updated models.
- Additional features or rewrites of current features are accompanied by tests.
- New features are demonstrated in a model, so folks can understand more easily.


Licensing
--------

The License of this project is located in `LICENSE`_. By submitting a contribution to this project, you are agreeing that your contributions under this license and
with this waiver of copyright interest.

.. _`LICENSE` : https://github.com/projectmesa/mesa/blob/master/LICENSE


Special Thanks
--------

A special thanks to the following projects who offered inspiration for this contributing file.

- `Django`_
- `18F's FOIA`_
- `18F's Midas`_

.. _`Django` : https://github.com/django/django/blob/master/CONTRIBUTING.rst
.. _`18F's FOIA` : https://github.com/18F/foia-hub/blob/master/CONTRIBUTING.md
.. _`18F's Midas` : https://github.com/18F/midas/blob/devel/CONTRIBUTING.md

