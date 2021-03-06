#!/usr/bin/python

import sys


def main():
    last_key = None
    running_total = 0

    for input_line in sys.stdin:
        input_line = input_line.strip()

        try:
            this_key, value = input_line.split('\t', 1)
            value = int(value)
        except:
            continue

        if last_key == this_key:
            running_total += value
        else:
            if last_key:
                print("%s\t%d" % (last_key, running_total))
            running_total = value
            last_key = this_key

    if last_key == this_key:
        print("%s\t%d" % (last_key, running_total))


if __name__ == "__main__":
    main()
