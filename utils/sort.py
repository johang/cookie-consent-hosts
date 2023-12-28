#!/usr/bin/env python

from collections import defaultdict
from sys import argv


class Host:
    def __init__(self, address, hostnames):
        dots = hostnames[0].rsplit(".", 3)
        assert(len(dots) >= 2)
        self.address = address
        self.hostnames = hostnames
        self.domain = ".".join(dots[-2:])

    @staticmethod
    def parse(line):
        parts = line.split(" ")
        assert(len(parts) >= 2)
        return Host(parts[0], parts[1:])

    def __repr__(self):
        return f"{self.address} {self.hostnames[0]}"


for arg in argv[1:]:
    hostnames = defaultdict(list)

    with open(arg, "r") as f:
        key = "#"
        for line in f:
            line = line.strip()
            if line.startswith("# "):
                key = line
            elif line and not line.startswith("#"):
                hostnames[key].append(Host.parse(line))

    with open(arg, "w") as f:
        first = True
        for key, hosts in hostnames.items():
            if not first:
                f.write("\n")
            f.write(key + "\n")
            first = False
            for host in sorted(hosts, key=lambda h: h.domain):
                f.write(str(host) + "\n")
