#! /usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint
import argparse
import sys

from configobj import ConfigObj


def read_arguments(args):
    parser = argparse.ArgumentParser(
        description="""
        Open a config file in .ini format files, replace, add, comment or remove values.
        """.strip(),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-f', '--filename',
        dest='filename',
        type=str,
        action='store',
        help='The file path to parse config',
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        dest='verbose',
        default=False,
        help='Show the full detail of changes status.'
    )

    parser.add_argument(
        '-r', '--remove',
        action='store',
        dest='remove',
        default='',
        help='Remove the option argument from the default section if no -s <section>. Applies before --add.'
    )

    parser.add_argument(
        '-p', '--print',
        action='store_true',
        dest='print',
        default=False,
        help='Print the value of the option passed in the argument.'
    )

    parser.add_argument(
        '-a', '--add',
        action='store',
        dest='add',
        type=str,
        default='',
        help='Adds the option=value to the default section if no -s <section>. If the option exists then overwrites.'
    )

    parser.add_argument(
        '-c', '--comment',
        action='store',
        dest='comment',
        type=str,
        default='',
        help='Comments the selected options by parameter, separated by comma.\nEj: "comment one, comment two"\nAll '
             'addend over the current option. '
    )

    parser.add_argument(
        '-s', '--section',
        action='store',
        dest='section',
        type=str,
        default='',
        help='Selected section to apply changes. Default, first section.'
    )

    options = parser.parse_args(args)
    return options


def main(args):
    options = read_arguments(args)
    config = ConfigObj(options.filename)

    verbose = False
    if options.verbose:
        verbose = True
        pprint('Full options: {}'.format(options))

    section = None
    if options.section:
        section = options.section
    else:
        if config.sections:
            section = config.sections[0]
    if verbose:
        pprint('Section: {}'.format(section))

    comments = None
    if options.comment:
        comm = options.comment.split(',')
        comments = map(str.strip, comm)
        if verbose:
            pprint('Comments: {}'.format(comments))

    if options.remove:
        rem = options.remove.strip()
        if verbose:
            pprint('Option to remove: {}'.format(rem))
        config[section].comments.update({
            rem: comments,
        })
        del config[section][rem]

    if options.add:
        key_val = options.add.split('=')
        if len(key_val) != 2:
            pprint('Invalid parameter value... {}'.format(options.add))
            exit(-1)
        opt = key_val[0].strip()
        val = key_val[1].strip()
        if verbose:
            pprint('Option to add or update: {}\nValue: '.format(opt, val))
        config[section][opt] = val
        config[section].comments.update({
            opt: comments,
        })

    config.write()


if __name__ == '__main__':
    main(sys.argv[1:])
