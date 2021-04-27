# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020-2021 Óscar García Amor <ogarcia@connectical.com>
#
# Distributed under terms of the GNU GPLv3 license.

from lpacli.config import config
from lpacli.commands.get_pass import get_pass

import argparse
import logging

def main():
    # Set loglevel equivalents for argument parser
    log_levels = {
            0: logging.WARNING,
            1: logging.INFO,
            2: logging.DEBUG }

    # Create argument parser to get options via arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0, help='be verbose (add more v to increase verbosity)')
    parser.add_argument('-s', '--settings', action='store_true', help='print site settings instead of password')
    parser.add_argument('site', help='site to obtain password or ls to list')
    parser.set_defaults(func=get_pass)

    args = parser.parse_args()

    # Maximum loglevel is 3 if user sends more vvv we ignore it
    args.verbose = 2 if args.verbose >= 2 else args.verbose

    # Set loglevel via argument or environment (untouched warning by default)
    log_level = log_levels[args.verbose]
    logging.basicConfig(level=log_level)
    logger = logging.getLogger('lpacli')
    logger.info('Setting loglevel to {}'.format(logging.getLevelName(log_level)))
    logger.debug('Parsed arguments, settings: "{}", site: "{}"'.format(args.settings, args.site))

    # Configure app
    config.configure()

    # Run main app
    args.func(args)
