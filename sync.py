#! /usr/bin/env python
# coding: utf-8
# vim:fenc=utf-8
# created_on: 2019-11-24 02:10

"""Sync."""


import os
import re


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


class Merger(object):
    def __init__(self, destination, source):
        self.destination = destination
        self.source = source
        self.merged = list()

        self.merge_policies = {MERGE_POLICIES.APPEND, }

    def sort(self, **by):
        pass

    def merge(self):
        self.merged = list()
        if MERGE_POLICIES.UNIQUE in self.merge_policies:
            self.merged.extend(set(self.destination))
            self.merged.extend(set(self.source))
            self.merged = set(self.merged)


ZSH_HIST_EPOCH_PATTERN = r'^: \d{10}:\d+;(.*)'
ZSH_HIST_EPOCH_FORMAT = re.compile(ZSH_HIST_EPOCH_PATTERN)


class FILE_STYLE(object):
        BASH = 0
        ZSH_WITH_EPOCH = 1


class ShellHistoryFile(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.lines = list()
        self._style = None
        self._read_lines()
        self._sanitize()

    def _read_lines(self):
        with open(self.filepath, 'r') as fp:
            self.lines = fp.readlines()

    def _sanitize(self):
        self.lines = [line.strip() for line in self.lines if line not in (None, '', ' ')]

    @property
    def style(self):
        if self._style:
            return self._style

        if ZSH_HIST_EPOCH_FORMAT.match(self.lines[0]):
            self._style = FILE_STYLE.ZSH_WITH_EPOCH            
    
        return self._style

    def convert(self, to=FILE_STYLE.BASH):
        converted_lines = list()
        if self.style == FILE_STYLE.ZSH_WITH_EPOCH and to == FILE_STYLE.BASH:
            for line in self.lines:
                match = ZSH_HIST_EPOCH_FORMAT.match(line)
                if match:
                    group = match.groups()
                    if group:
                        converted_lines.append(group[0])
                    else:
                        converted_lines.append(line)
                else:
                    converted_lines.append(line)
       
        self.lines = converted_lines
        self._sanitize()
        return self

    def unique(self):
        self.lines = set(self.lines)
        return self


if __name__ == '__main__':
    REMOTE_FILE = os.path.join(os.environ['WORKSPACE'], 'secret', 'self', 'terminal-history', '.zsh_history')
    LOCAL_FILE = os.path.join(os.environ['HOME'], '.zsh_history')

    remote = ShellHistoryFile(REMOTE_FILE).convert().unique()
    local = ShellHistoryFile(LOCAL_FILE).convert().unique()
    
    m = Merger(local.lines, remote.lines)
    m.merge_policies.update({MERGE_POLICIES.APPEND, MERGE_POLICIES.UNIQUE})
    m.merge()

    with open('.zsh_history', 'w') as fp:
        fp.writelines("\n".join(m.merged))
    
