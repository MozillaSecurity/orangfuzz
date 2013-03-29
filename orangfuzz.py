#!/usr/bin/env python
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import random
import sys

if sys.version_info >= (2, 6):
    from argparse import ArgumentParser
else:
    raise Exception('orangfuzz has only been tested on Python 2.7 and above.')

# Framework (orangutan) syntax:
# tap [x] [y] [num times] [duration of each tap in msec]
# sleep [duration in msec]
# drag [start x] [start y] [end x] [end y] [num steps] [duration in msec]

TAP_ACTION = 'tap'
SLEEP_ACTION = 'sleep'
DRAG_ACTION = 'drag'
ACTION_CHOICES = (TAP_ACTION, SLEEP_ACTION, DRAG_ACTION)


def parseArgs():
    parser = ArgumentParser(description='Create a randomly-generated orangutan script.')
    parser.add_argument('-l', '--lines', default=10000, type=int,
                        help='Set the number of lines to generate.')
    parser.add_argument('-o', '--output', default='script.txt',
                        help='Set the desired output file.')
    parser.add_argument('-s', '--seed', type=float,
                        help='Set the desired seed, else default values are randomly generated.')
    args = parser.parse_args(sys.argv[1:])
    return args


##################
# Device support #
##################

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
                            ['1', '2000'])
        #                   ['1', str(rnd.randint(2000, 10000))])


class Unagi(OrangutanDevice):
    def __init__(self):
        super(Unagi, self).__init__()
        self.setMaxHorizPixels(320)
        self.setMaxVertPixels(520)
        self.setHomeKeyLocation([44, 515])


##################
# Pre-population #
##################

def prepopulateStart(dvc, rnd, lines):
    # We should also ensure B2G is in a reset state, before/after(?) the FTE wizard.
    lines.append(dvc.getHomeKeyTap(rnd))
    return lines


###################
# Line generation #
###################

def generateLines(args, dvc, rnd, outputLines):
    count = 1
    sleepAllowed = True

    while (count <= args.lines):
        if count % 1000 == 0:
            outputLines.append(dvc.getHomeKeyLongPress(rnd))
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
        elif (actionNow == SLEEP_ACTION):
            if sleepAllowed:
                outputLines.append(' '.join(str(x) for x in [
                    SLEEP_ACTION,
                    rnd.randint(100, 3000)
                ]))
                sleepAllowed = False
                count += 1
        else:
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
        #else:
        #    raise Exception('Unknown action: ' + actionNow)

    return outputLines


#################
# Miscellaneous #
#################

def writeToFile(outputFile, lines):
    lines.append('')  # Ending line break
    with open(outputFile, 'wb') as f:
        f.write('\n'.join(lines))


def main():
    args = parseArgs()
    args.seed = random.random() if args.seed == None else args.seed
    rndObj = random.Random(str(args.seed))

    orangDevice = Unagi()
    allLines = []

    allLines.append('# Current seed is: ' + str(args.seed))
    allLines = prepopulateStart(orangDevice, rndObj, allLines)
    allLines = generateLines(args, orangDevice, rndObj, allLines)

    writeToFile(args.output, allLines)


if __name__ == '__main__':
    main()
