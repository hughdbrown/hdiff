#!/usr/bin/env python3
from hashlib import sha1
from collections import defaultdict

import click

class DiffFile:
    def __init__(self, filename):
        self.filename = filename
        with open(filename, "r", encoding="utf-8") as handle:
            self.lines = [line.rstrip() for line in handle]
            self.hashes = [
                sha1(line.encode('utf-8')).hexdigest()
                for line in self.lines
            ]

    def diff(self, other):
        matches = []

        self_end, other_end = len(self.lines) - 1, len(other.lines) - 1
        upper = min(self_end, other_end)

        self_left, self_right, other_left, other_right = None, None, None, None

        # Trim from the start
        for i in range(upper + 1):
            print(
                f"left_ {self.lines[i]}\n"
                f"right {other.lines[i]}\n"
                f"----- ({i}, {i})"
            )
            if self.hashes[i] != other.hashes[i]:
                if i > 0:
                    matches.append(([0, i - 1], [0, i - 1]))
                    self_left = self_right = i - 1
                break

        # Trim from the end
        for i in range(upper):
            print(
                f"left_ {self.lines[self_end - i]}\n"
                f"right {other.lines[other_end - i]}\n"
                f"----- ({self_end - i}, {other_end - i})"
            )
            if self.hashes[self_end - i] != other.hashes[other_end - i]:
                if i > 0:
                    matches.append(([self_end - i, self_end], [other_end - i, other_end]))
                    self_right = self_end - i
                    other_right = other_end - i
                break

        self_count = defaultdict(list)
        other_count = defaultdict(list)

        l, r = ((self_left or 0), (self_right or self_end)), ((other_left or 0), (other_right or other_end))
        for i in range(self_left, self_end + 1):
            self_count[self.hashes[i]].append(i)

        for i in range(other_left, other_end + 1):
            other_count[other.hashes[i]].append(i)

        self_unique = set(self_count) - set(other_count)
        other_unique = set(
        return matches


@click.command()
@click.argument('file1')
@click.argument('file2')
def main(file1, file2):
    df1 = DiffFile(file1)
    df2 = DiffFile(file2)
    m = df1.diff(df2)
    print(m)

if __name__ == '__main__':
    main()
