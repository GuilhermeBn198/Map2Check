#!/usr/bin/env python3

# This file is part of the Test-Comp test format,
# an exchange format for test suites:
# https://gitlab.com/sosy-lab/software/test-format
#
# SPDX-FileCopyrightText: 2018-2019 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

from lxml import etree
import glob
from urllib import request

class DTDResolver(etree.Resolver):

    def resolve(self, url, id, context):
        if url.startswith("http"):
            with request.urlopen(url) as inp:
                dtd_content = inp.read()
            return self.resolve_string(dtd_content, context)
        else:
            return super().resolve(url, id, context)


if __name__ == "__main__":
    parser = etree.XMLParser(dtd_validation=True)
    parser.resolvers.add(DTDResolver())

    for xml in glob.glob('*.xml'):
        etree.parse(xml, parser)
    print("examples are valid!")
