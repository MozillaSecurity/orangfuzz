#!/usr/bin/env python
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Functions that help to define the prepopulated state of the phone are here.


def prepopulateStart(dvc, rnd, lines):
    '''Prepopulate the phone as desired.'''
    # We should also ensure B2G is in a reset state, before/after(?) the FTE wizard.
    # FIXME: Make use of b2gpopulate? https://github.com/mozilla/b2gpopulate
    lines.append(dvc.getHomeKeyTap(rnd))
    return lines

if __name__ == '__main__':
    pass
