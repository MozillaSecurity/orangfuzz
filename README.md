orangfuzz
=========

An experimental UI fuzzer based on the orangutan framework for Firefox OS devices.

Python 2.7 and above is required.

To run:
./orangfuzz.py

It outputs to a file called script-orangutan-<random seed>.txt by default.

e.g. with a seed of 223798447 and adb detecting the device, run:

# push the script to the device
$ adb push ~/trees/orangfuzz/script-orangutan-223798447.txt /mnt/sdcard/
# Execute the script with the compiled orangutan binary in /data
$ adb shell /data/orng /dev/input/event0 /mnt/sdcard/script-orangutan-223798447.txt

To get a list of options:
./orangfuzz.py --help
