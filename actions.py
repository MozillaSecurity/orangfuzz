#!/usr/bin/env python
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Functions / constants related to orangutan actions are here.

from utils import countWithDesc

TAP_ACTION = 'tap'
SLEEP_ACTION = 'sleep'
DRAG_ACTION = 'drag'
# FIXME: What about pinch actions?
ACTION_CHOICES = (TAP_ACTION, SLEEP_ACTION, DRAG_ACTION)


def getRandomSleep(rnd, count):
    '''Returns sleeps of random durations.'''
    #return ' '.join(str(x) for x in [countWithDesc(count, 'Sleep action') + SLEEP_ACTION, rnd.randint(100, 3000)])
    return ' '.join(str(x) for x in [SLEEP_ACTION, rnd.randint(100, 3000)])


def getDragToRightHomescreen(rnd, count):
    '''Returns a drag action to the homescreen on the right side.'''
    # Fixed to Unagi for the moment.
    return ' '.join(str(x) for x in [countWithDesc(count, 'Drag action') + DRAG_ACTION, 118, 53, 36, 108, 12, 99])

if __name__ == '__main__':
    pass
