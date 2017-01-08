#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shlex
import subprocess as sp


class Brain:
    def __init__(self, config):
        from whoosh.fields import TEXT, ID, Schema
        from whoosh.index import create_in, open_dir
        self.editor = config.get('brain', 'editor')
        self.result_limit = int(config.get('brain', 'result-limit'))
        self.storage_path = os.path.expanduser(config.get('brain', 'storage'))
        self.index_path = os.path.expanduser(config.get('brain', 'index'))
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
        if not os.path.exists(self.index_path):
            os.makedirs(self.index_path)
            schema = Schema(entry=ID(stored=True, unique=True), content=TEXT(stored=True))
            self.index = create_in(self.index_path, schema)
            self.index_all()
        else:
            self.index = open_dir(self.index_path)

    @staticmethod
    def entry_name():
        import random
        import string
        from datetime import datetime
        date_str = datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
        random_str = ''.join(random.choice(string.hexdigits) for _ in range(8)).upper()
        return date_str + '_' + random_str

    def index_entry(self, entry_path, entry_name):
        if not os.path.isfile(entry_path):
            return False
        writer = self.index.writer()
        with open(entry_path) as entry_file:
            entry_content = ''.join(entry_file.readlines())
        writer.update_document(entry=entry_name, content=entry_content)
        writer.commit()
        return True

    def index_all(self):
        for entry in os.listdir(self.storage_path):
            entry_path = os.path.join(self.storage_path, entry)
            entry_name = os.path.splitext(entry)[0]
            if os.path.isfile(entry_path) and os.path.splitext(entry)[-1] == '.entry':
                self.index_entry(entry_path, entry_name)

    def dump_entry(self):
        return self.edit_entry(self.entry_name())

    def edit_entry(self, entry_name):
        entry_path = os.path.join(self.storage_path, entry_name + '.entry')
        cmd = shlex.split(self.editor + ' ' + entry_path)
        if sp.call(cmd):
            return False
        return self.index_entry(entry_path, entry_name)

    def edit_result_list(self, results):
        no_color = '\033[0m'
        hi_color = '\033[0;32m'
        bold = '\033[1m'

        from whoosh import highlight

        class TerminalFormatter(highlight.Formatter):
            def __init__(self):
                pass

            def format_token(self, text, token, replace=False):
                return hi_color + highlight.get_text(text, token, replace) + no_color

        results.formatter = TerminalFormatter()
        print('multiple memories found (return to close):')
        for i, result in enumerate(results):
            print(bold + str(i + 1) + no_color + '. ...' + result.highlights('content') + '...')
        while True:
            try:
                num = input('number to open: ')
                if len(num) == 0:
                    return None
                res_index = int(num) - 1
                if 0 <= res_index < len(results):
                    self.edit_entry(results[res_index]['entry'])
            except ValueError:
                continue
            except KeyboardInterrupt:
                return None

    def remember(self, tokens):
        from whoosh.qparser import QueryParser
        parser = QueryParser('content', schema=self.index.schema)
        query = parser.parse(' '.join(['*' + token + '*' for token in tokens]))
        with self.index.searcher() as searcher:
            results = searcher.search(query, limit=self.result_limit)
            if len(results) == 1:
                self.edit_entry(results[0]['entry'])
            elif len(results) > 1:
                self.edit_result_list(results)
            else:
                return False
        return True


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser('braindump')
    parser.add_argument('operation', help='the operation: dump, remember (rem)')
    parser.add_argument('terms', help='search terms (for remember operation)', nargs='*')
    parser.add_argument('--config', default='~/.brain.conf', help='config file (defaults to ~/.brain.conf)')
    return parser.parse_args()


def guess_editor(config_path):
    editors = ['vim', 'emacs', 'nano']
    for editor in editors:
        cmd = shlex.split('hash ' + editor)
        if not sp.call(cmd, shell=True):
            return editor
    print('failed to find an editor, please set value manually in ' + config_path)
    return ''


def get_conf(config_path):
    from configparser import ConfigParser
    expanded_path = os.path.expanduser(config_path)
    if not os.path.isfile(expanded_path):
        config = ConfigParser()
        config.add_section('brain')
        config.set('brain', 'storage', '~/.brain')
        config.set('brain', 'index', '~/.brain/index')
        config.set('brain', 'editor', guess_editor(config_path))
        config.set('brain', 'result-limit', '10')
        with open(expanded_path, 'w') as configfile:
            config.write(configfile)
        return config
    config = ConfigParser()
    config.read(expanded_path)
    return config


def main():
    args = get_args()
    config = get_conf(args.config)
    brain = Brain(config)
    if args.operation == 'dump':
        if not brain.dump_entry():
            print('unable to dump entry')
    elif args.operation == 'remember' or args.operation == 'rem':
        if len(args.terms) < 1:
            print('no terms given')
        else:
            if not brain.remember(args.terms):
                print('no entries found')


if __name__ == "__main__":
    main()
