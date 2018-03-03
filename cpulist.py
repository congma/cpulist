#!/usr/bin/env python
"""Dump CPU affinity information as a tree."""


import sys
import collections
import re
import json


ORDER = {"physical id": 0, "core id": 1, "processor": 2}
PATTERN = "^(" + "|".join(ORDER.keys()) + ")"
FILTER_RE = re.compile(PATTERN)
ISLEAF = 0b001
ISFIRST = 0b010
ISLAST = 0b100


class DictTree(object):
    """Tree stucture implemented using dict. No need for a Node() class, but
    each key must be hashable, and sibling of the same level must be unique.
    The order of siblings is lost.
    """

    def __init__(self):
        """Create root node."""
        self._root = {}
        return None

    def add(self, inputlist):
        """Add the nodes specified in inputlist to the tree.The nth element of
        inputlist is added in the (n+1)th level (root is level 0).
        """
        _add(self._root, inputlist)
        return None

    def dumpjson(self, sort_keys=True, **kwargs):
        """Return a string dump in JSON format, with keys sorted by default."""
        return json.dumps(self._root, sort_keys=sort_keys, **kwargs)

    def dumpascii(self, **kwargs):
        """Return a string dump of an ascii drawing of the tree."""
        return _dumpascii(_tokenize(self._root, **kwargs))


class CpuTree(DictTree):
    """Tree representing the CPUs found in /proc/cpuinfo."""

    def __init__(self):
        super(CpuTree, self).__init__()
        for cpu in _part3(_filter_cpuinfo()):
            self.add(cpu)

    @staticmethod
    def _cpu_sort_key(node):
        """Default sort key for presenting sibling CPU nodes."""
        label = node[0]
        # Take 1st element (string), cut at last colon, take the 2nd field
        # (number), remove any whitespace, and parse as number.
        return int(label.rsplit(sep=":", maxsplit=1)[1].strip())

    def dumpascii(self, sibling_sort_key=None):  # pylint: disable=W0221
        """Return a string dump of an ascii drawing of the tree.
        The optional argument "sibling_sort_key" is a callable key function
        that specifies the order in which siblings are sorted.  If it is not
        specified or is "None", the default order is used.
        """
        if sibling_sort_key is None:
            key = self._cpu_sort_key
        else:
            key = sibling_sort_key
        return super(CpuTree, self).dumpascii(sibling_sort_key=key)


def _add(node, inputlist):
    """Add elements in inputlist to the tree, rooted at given node.  Leaf nodes
    have an empty dictionary as child.  The nth element of inputlist is added
    to the (n + 1)th level descending from node.
    """
    try:
        head = inputlist[0]
    except IndexError:
        return
    tail = inputlist[1:]
    nextnode = node.setdefault(head, {})
    _add(nextnode, tail)


def _tokenize(node, sibling_sort_key=None):
    """Generator that traverses a tree in pre-order from node.
    Each yielded value is a tuple of (nodekey, depth, flags).
    flags is a bitwise-or'ed mask of following bits:
        0b001: node is a leaf
        0b010: node is first among siblings
        0b100: node is last among siblings (can be set with 0b010).
    The siblings are sorted by the key function sibling_sort_key.
    """
    trackstack = []
    this = node
    depth = 0
    yield "*", 0, (ISFIRST | ISLAST)  # root
    while trackstack or this:
        children = this.items()
        if children:
            # NOTE: Siblings are reversed because the list "trackstack"
            # operates on the tail as a stack.
            children.sort(key=sibling_sort_key, reverse=True)
            numchi = len(children)
            chiflags = [0] * numchi
            chiflags[0] |= ISLAST
            chiflags[-1] |= ISFIRST
            depth += 1
            tmp = children[-1]  # first child
            thisflag = chiflags[-1]
            tail = children[:-1]
            trackstack.extend(zip(tail,
                                  [depth] * (numchi - 1),
                                  chiflags[:-1]))
        else:
            tmp, depth, thisflag = trackstack.pop()  # Load depth and flags.
        yield tmp[0], depth, thisflag | (ISLEAF if not tmp[1] else 0)
        this = tmp[1]   # Advance to next.


def _symbol(label, flags, taillen=1):
    """Generate drawing symbol using a token's label and flags."""
    tail = "\n" if (flags & ISLEAF) else "-" * taillen
    isonlychild = (flags & ISFIRST) and (flags & ISLAST)
    if isonlychild:
        stem = "-"
    elif flags & ISFIRST:
        stem = "+"
    elif flags & ISLAST:
        stem = "`"
    else:
        stem = "|"
    return "%s-%s%s" % (stem, label, tail)


def _dumplines(tokenstream):
    """Draw using the input tokenstream iterator.  Yield a string for each line
    of the drawing.
    """
    linebuf = []
    # Possible depths where a vertical connecting bar should be drawn
    marks = set()
    columnwidths = collections.defaultdict(lambda: 0)
    for label, depth, flags in tokenstream:
        # Set or clear vertical bar positions (column No.) for next line.
        if not flags & ISLAST:
            marks.add(depth)
        else:
            marks.discard(depth)
        symbol = _symbol(label, flags)
        columnwidths[depth] = len(symbol)
        if flags & ISFIRST:  # set position for next column
            indentstring = ""   # no indentation
        else:  # need indent
            indent = []
            for i in xrange(depth):  # for each indentation level
                tmpl = [" "] * columnwidths[i]  # "array" of blanks as filler
                if i in marks:  # vertical bar connectors
                    tmpl[0] = "|"
                indent.extend(tmpl)
            indentstring = "".join(indent)
        linebuf.append("%s%s" % (indentstring, symbol))
        if flags & ISLEAF:
            yield "".join(linebuf)
            linebuf = []


def _dumpascii(tokenstream):
    """Convert tokenstream to ascii drawing."""
    return "".join(_dumplines(tokenstream))


def _filter_cpuinfo():
    """Return a list of tuples, each of which looks like ("processor", 0), etc.
    """
    tmplist = []
    with open("/proc/cpuinfo", "r") as cpuinfo:
        for line in cpuinfo:
            if FILTER_RE.match(line):
                key, _, val = (x.strip() for x in line.partition(":"))
                tmplist.append((key, int(val)))
    return tmplist


def _part3(inputlist):
    """Return a list of id-lists.

    An id-list is a representation of a particular CPU's id.  The id-list is a
    list of ids in ascending order of each id's level.  Each id looks like
    "processor: 0", "core id: 1" etc.

    The returned list itself is not necessarily sorted in any particular order.
    """
    length = len(inputlist)
    tmplist = []
    for i in xrange(length / 3):
        tmptriplet = inputlist[i * 3:(i + 1) * 3]
        tmptriplet.sort(key=lambda t: ORDER[t[0]])
        tmplist.append(["%s: %s" % x for x in tmptriplet])
    return tmplist


def test():
    """Self-test"""
    cpus = CpuTree()
    sys.stdout.write(cpus.dumpascii())
    return None


if __name__ == "__main__":
    test()
