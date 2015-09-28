#! python
# -*- coding: UTF-8 -*-
#
# Copyright 2015 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl

import os
import re
import unittest

import compas


mydir = os.path.dirname(__file__)
readme_path = os.path.join(mydir, '..', 'README.rst')
tutorial_path = os.path.join(mydir, '..', 'doc', 'tutorial.rst')


class Doctest(unittest.TestCase):

    def test_README_version_opening(self):
        ver = compas.__version__
        header_len = 20
        mydir = os.path.dirname(__file__)
        with open(readme_path) as fd:
            for i, l in enumerate(fd):
                if ver in l:
                    break
                elif i >= header_len:
                    msg = "Version(%s) not found in README %s header-lines!"
                    raise AssertionError(msg % (ver, header_len))

    def test_README_version_cmdline(self):
        ver = compas.__version__
        mydir = os.path.dirname(__file__)
        with open(readme_path) as fd:
            ftext = fd.read()
            m = re.search(
                r'co2mpas --version\s+%s' % ver, ftext, re.MULTILINE | re.IGNORECASE)
            self.assertIsNotNone(m,
                                 "Version(%s) not found in README cmd-line version-check!" %
                                 ver)