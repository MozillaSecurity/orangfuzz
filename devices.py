#!/usr/bin/env python
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Define devices supported by the orangutan framework here.
# More information on orangutan: https://github.com/wlach/orangutan

from actions import TAP_ACTION
from utils import countDescAction


class OrangutanDevice(object):
    '''An OrangutanDevice assumes that a compiled orangutan binary has been "adb push"ed to the
    device. See https://github.com/wlach/orangutan for more details.'''
    def setMaxHorizPixels(self, hpx):
        '''Sets the maximum horizontal pixels.'''
        self.hpx = hpx
    def getMaxHorizPixels(self):
        '''Gets the maximum horizontal pixels.'''
        return self.hpx
    def setMaxVertPixels(self, vpx):
        '''Sets the maximum vertical pixels.'''
        self.vpx = vpx
    def getMaxVertPixels(self):
        '''Gets the maximum vertical pixels.'''
        return self.vpx
    def setHomeKeyLocation(self, loc):
        '''Sets the location of the home key.'''
        # See bug 838267, a bug on supporting the HOME key for the orangutan library
        assert isinstance(loc, list), 'Must be a list because we concatenate this later.'
        self.loc = loc
    def getHomeKeyLocation(self):
        '''Gets the location of the home key.'''
        return self.loc
    def getHomeKeyTap(self, rnd, count):
        '''Trigger a tap on the home key.'''
        return ' '.join([countDescAction(count, 'Home key tap', TAP_ACTION)] +
                            [str(x) for x in self.getHomeKeyLocation()] +
                            ['1', str(rnd.randint(50, 1000))]
                        )
    def getHomeKeyLongPress(self, rnd, count):
        '''Trigger a long press on the home key, defined as >= 2 seconds.'''
        return ' '.join([countDescAction(count, 'Home key long press', TAP_ACTION)] +
                            [str(x) for x in self.getHomeKeyLocation()] +
                            ['1', str(rnd.randint(2000, 10000))]
                        )


class Unagi(OrangutanDevice):
    '''Unagi devices were available for dogfooding.'''
    def __init__(self):
        '''Unagi devices have 320x520 resolution.'''
        super(Unagi, self).__init__()
        self.setMaxHorizPixels(320)
        self.setMaxVertPixels(520)
        self.setHomeKeyLocation([44, 515])

if __name__ == '__main__':
    pass
