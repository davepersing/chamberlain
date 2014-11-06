#!/usr/bin/env python

import argparse
import chamberlain.cli.command as cli_commands
import chamberlain.version as chamberlain_version
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def version():
    return "Chamberlain version: %s" % \
        chamberlain_version.version_info.version_string()


def command_hash():
    return {
        "list-repos": cli_commands.ListRepoCommand
    }


def create_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c',
                        '--config',
                        dest='config',
                        help='Configuration file to load.')

    parser.add_argument('--version',
                        dest='version',
                        action='version',
                        version=version(),
                        help='Show version')

    cmd_parsers = parser.add_subparsers(help="chamberlain commands",
                                        dest="command")

    for cmd, cmd_class in command_hash().items():
        cmd_obj = cmd_class(logger)
        command_parser = cmd_parsers.add_parser(cmd,
                                                help=cmd_obj.description())
        cmd_obj.configure_parser(command_parser)

    return parser


def main(argv=None):
    parser = create_parser()
    options = parser.parse_args(argv)

    if not options.command:
        parser.error("Must specify a 'command' to be performed")

    command_hash()[options.command](logger, options.config).execute(options)


if __name__ == '__main__':
    sys.path.insert(0, '.')
    main()