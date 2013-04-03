#!/usr/bin/env python
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from actions import TAP_ACTION


class OrangutanDevice(object):
    def setMaxHorizPixels(self, hpx):
        self.hpx = hpx
    def getMaxHorizPixels(self):
        return self.hpx
    def setMaxVertPixels(self, vpx):
        self.vpx = vpx
    def getMaxVertPixels(self):
        return self.vpx
    def setHomeKeyLocation(self, loc):
        # See bug 838267, a bug on supporting the HOME key for the orangutan library
        assert isinstance(loc, list), 'Must be a list because we concatenate this later.'
        self.loc = loc
    def getHomeKeyLocation(self):
        return self.loc
    def getHomeKeyTap(self, rnd):
        return ' '.join([TAP_ACTION] + [str(x) for x in self.getHomeKeyLocation()] +
                            ['1', str(rnd.randint(50, 1000))])
    def getHomeKeyLongPress(self, rnd):
        return ' '.join([TAP_ACTION] + [str(x) for x in self.getHomeKeyLocation()] +
                           ['1', str(rnd.randint(2000, 10000))])


class Unagi(OrangutanDevice):
    def __init__(self):
        super(Unagi, self).__init__()
        self.setMaxHorizPixels(320)
        self.setMaxVertPixels(520)
        self.setHomeKeyLocation([44, 515])

if __name__ == '__main__':
    pass
