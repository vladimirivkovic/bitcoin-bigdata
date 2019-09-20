#!/usr/bin/python

import sys


def main():
    for line in sys.stdin:
        fields = line.strip().split(',')
        if len(fields) == 6 and fields[5] is not None:
            print("%s\t%s" % (fields[4], fields[5]))


if __name__ == "__main__":
    main()
