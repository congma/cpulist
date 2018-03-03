`cpulist.py` -- display CPU affinity information as ASCII art.

Summary
-------

With this Python script, you get a visual display of the layout of physical
CPUs, CPU cores and processor ID's.  It is straightforward to see which
processors/cores are siblings.

Requirements
------------

This script runs on Linux by reading the file `/proc/cpuinfo`.  The format of
that file depends on the architecture, and this script seems to work for Intel
x86/x86\_64 systems.  It is probably straightforward to add support for other
systems.

Example
-------

Example output from a machine with 4 set of CPUs, each with 10 cores, and
each core capable of running 2 threads (Intel HT):

    --*-+-physical id: 0-+-core id: 0-+-processor: 0
        |                |            `-processor: 40
        |                |-core id: 1-+-processor: 4
        |                |            `-processor: 44
        |                |-core id: 2-+-processor: 8
        |                |            `-processor: 48
        |                |-core id: 8-+-processor: 12
        |                |            `-processor: 52
        |                |-core id: 9-+-processor: 16
        |                |            `-processor: 56
        |                |-core id: 16-+-processor: 20
        |                |             `-processor: 60
        |                |-core id: 17-+-processor: 24
        |                |             `-processor: 64
        |                |-core id: 18-+-processor: 28
        |                |             `-processor: 68
        |                |-core id: 24-+-processor: 32
        |                |             `-processor: 72
        |                `-core id: 25-+-processor: 36
        |                              `-processor: 76
        |-physical id: 1-+-core id: 0-+-processor: 1
        |                |            `-processor: 41
        |                |-core id: 1-+-processor: 5
        |                |            `-processor: 45
        |                |-core id: 2-+-processor: 9
        |                |            `-processor: 49
        |                |-core id: 8-+-processor: 13
        |                |            `-processor: 53
        |                |-core id: 9-+-processor: 17
        |                |            `-processor: 57
        |                |-core id: 16-+-processor: 21
        |                |             `-processor: 61
        |                |-core id: 17-+-processor: 25
        |                |             `-processor: 65
        |                |-core id: 18-+-processor: 29
        |                |             `-processor: 69
        |                |-core id: 24-+-processor: 33
        |                |             `-processor: 73
        |                `-core id: 25-+-processor: 37
        |                              `-processor: 77
        |-physical id: 2-+-core id: 0-+-processor: 2
        |                |            `-processor: 42
        |                |-core id: 1-+-processor: 6
        |                |            `-processor: 46
        |                |-core id: 2-+-processor: 10
        |                |            `-processor: 50
        |                |-core id: 8-+-processor: 14
        |                |            `-processor: 54
        |                |-core id: 9-+-processor: 18
        |                |            `-processor: 58
        |                |-core id: 16-+-processor: 22
        |                |             `-processor: 62
        |                |-core id: 17-+-processor: 26
        |                |             `-processor: 66
        |                |-core id: 18-+-processor: 30
        |                |             `-processor: 70
        |                |-core id: 24-+-processor: 34
        |                |             `-processor: 74
        |                `-core id: 25-+-processor: 38
        |                              `-processor: 78
        `-physical id: 3-+-core id: 0-+-processor: 3
                         |            `-processor: 43
                         |-core id: 1-+-processor: 7
                         |            `-processor: 47
                         |-core id: 2-+-processor: 11
                         |            `-processor: 51
                         |-core id: 8-+-processor: 15
                         |            `-processor: 55
                         |-core id: 9-+-processor: 19
                         |            `-processor: 59
                         |-core id: 16-+-processor: 23
                         |             `-processor: 63
                         |-core id: 17-+-processor: 27
                         |             `-processor: 67
                         |-core id: 18-+-processor: 31
                         |             `-processor: 71
                         |-core id: 24-+-processor: 35
                         |             `-processor: 75
                         `-core id: 25-+-processor: 39
                                       `-processor: 79
