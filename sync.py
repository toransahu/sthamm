#! /usr/bin/env python
# coding: utf-8
# vim:fenc=utf-8
# created_on: 2019-11-24 02:10

"""Sync."""

import os


__author__ = 'Toran Sahu <toran.sahu@yahoo.com>'
__license__ = 'Distributed under terms of the MIT license'


# TODO
'''
grab files
backup
understand file struct
merge
sort
update local
update remote
deploy
automate
  - fetch remote on startup
  - update local on startup
  - update remote <interval>
'''


class MERGE_POLICIES(object):
    APPEND = 0
    PREFIX = 1
    UNIQUE = 2


class FileMerge(object):
    def __init__(self, destination, source):
        self.destination = destination
        self.source = source

        self.merge_policies = {MERGE_POLICIES.APPEND, }

    def sort(self, **by):
        pass

    def merge(self):
        pass


class ShellHistoryFile(object):
    class FILE_FORMAT(object):
        BASH = 0
        ZSH_WITH_EPOCH = 1

    def __init__(self, filepath):
        self.filepath = filepath
        self.lines = list()
        self.read_lines()

    def read_lines(self):
        with open(self.filepath, 'r') as fp:
            self.lines = fp.readlines()

    @property
    def in_plain_style(self):
        pass

    def convert(self, format=FILE_FORMAT.BASH):
        pass

    def unique(self, overwrite=False):
        unique_lines = set(self.lines)
        if overwrite:
            self.lines = unique_lines
        return unique_lines 


if __name__ == '__main__':
    fm = FileMerge('local_file', 'remote_file')
    # fm.merge_policies.update({1, 2})
    # shf = ShellHistoryFile('local_file')
    shf = ShellHistoryFile('/home/toransahu/Desktop/a.txt')
    from pprint import pprint
    pprint("\n".join(shf.lines))
