#!/usr/bin/env python
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# orangfuzz is an experimental UI fuzzer based on the orangutan framework for Firefox OS devices.
#
# To run: ./orangfuzz.py
#
#  Framework (orangutan) syntax:
#  tap [x] [y] [num times] [duration of each tap in msec]
#  sleep [duration in msec]
#  drag [start x] [start y] [end x] [end y] [num steps] [duration in msec]

import math
import random
import sys

from actions import ACTION_CHOICES
from actions import DRAG_ACTION
from actions import SLEEP_ACTION
from actions import TAP_ACTION
from devices import Unagi
from prepopulation import prepopulateStart
from utils import writeToFile

if sys.version_info >= (2, 7):
    from argparse import ArgumentParser
else:
    raise Exception('orangfuzz has only been tested on Python 2.7 and above.')


def parseArgs():
    '''Parse arguments given to orangfuzz.'''
    parser = ArgumentParser(description='Create a randomly-generated orangutan script.')
    parser.add_argument('-l', '--lines', default=10000, type=int,
                        help='Set the number of lines to generate.')
    parser.add_argument('-o', '--outputFilename',
                        help='Set the desired output filename.')
    parser.add_argument('-s', '--seed', type=int,
                        help='Set the desired seed, else default values are randomly generated.')
    args = parser.parse_args(sys.argv[1:])
    return args


###################
# Line generation #
###################

def generateLines(args, dvc, rnd, outputLines):
    '''Get orangfuzz to generate lines.'''
    count = 1
    sleepAllowed = True

    while (count <= args.lines):
        # Tap the home key back to the home screen.
        if count % rnd.randint(1, 500) == 0:
            outputLines.append(dvc.getHomeKeyTap(rnd, count))
            sleepAllowed = True
            count += 1
            continue

        # Brings up the list of applications with a long press of the home key.
        if count % rnd.randint(1, 1000) == 0:
            outputLines.append(dvc.getHomeKeyLongPress(rnd, count))
            sleepAllowed = True
            count += 1
            continue

        actionNow = rnd.choice(ACTION_CHOICES)
        if actionNow == TAP_ACTION:
            outputLines.append(' '.join(str(x) for x in [
                TAP_ACTION,
                rnd.randint(1, dvc.getMaxHorizPixels()), rnd.randint(1, dvc.getMaxVertPixels()),
                rnd.randint(1, 3),
                rnd.randint(50, 1000)
            ]))
            sleepAllowed = True
            count += 1
        elif actionNow == SLEEP_ACTION:
            if sleepAllowed:
                outputLines.append(' '.join(str(x) for x in [
                    SLEEP_ACTION,
                    rnd.randint(100, 3000)
                ]))
                sleepAllowed = False
                count += 1
        elif actionNow == DRAG_ACTION:
            outputLines.append(' '.join(str(x) for x in [
                DRAG_ACTION,
                # Starting co-ordinates
                rnd.randint(1, dvc.getMaxHorizPixels()), rnd.randint(1, dvc.getMaxVertPixels()),
                # Ending co-ordinates
                rnd.randint(1, dvc.getMaxHorizPixels()), rnd.randint(1, dvc.getMaxVertPixels()),
                rnd.randint(10, 20),
                rnd.randint(10, 350)
            ]))
            sleepAllowed = True
            count += 1
        else:
            raise Exception('Unknown action: ' + actionNow)

    return outputLines


def main():
    '''Run orangfuzz and randomly generate lines for the desired device.'''
    args = parseArgs()
    if args.seed is None:
        args.seed = int(math.floor(random.random() * math.pow(2, 28)))
    rndObj = random.Random(args.seed)

    orangDevice = Unagi()
    allLines = []

    allLines = prepopulateStart(orangDevice, rndObj, allLines)
    allLines = generateLines(args, orangDevice, rndObj, allLines)

    writeToFile(args, allLines)


if __name__ == '__main__':
    main()
