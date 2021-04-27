# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020-2021 Óscar García Amor <ogarcia@connectical.com>
#
# Distributed under terms of the GNU GPLv3 license.

import logging
import os
import sys

logger = logging.getLogger(__name__)

class Config:
    def __init__(self):
        self.token_cache_file = os.path.join(os.environ.get('XDG_CACHE_HOME', os.path.join(os.path.expanduser('~'), '.cache')), 'lpacli/lpacli-token')
        self.store_token = True
        self.lesspass_token = None
        self.lesspass_host = None
        self.lesspass_user = None
        self.lesspass_pass = None

    def configure(self):
        # Get host from environment
        self.lesspass_host = os.environ.get('LESSPASS_HOST')
        if self.lesspass_host == None:
            sys.exit('You must configure LESSPASS_HOST environment variable')
        logger.debug('LESSPASS_HOST: {}'.format(self.lesspass_host))

        # Try to access to cache to read token
        if os.path.isdir(os.path.dirname(self.token_cache_file)):
            try:
                with open(self.token_cache_file, 'r') as reader:
                    logger.debug('Reading token file: {}'.format(self.token_cache_file))
                    self.lesspass_token = reader.read()
                # If file is empty set token to none
                self.lesspass_token = None if self.lesspass_token == '' or '\n' in self.lesspass_token else self.lesspass_token
            except FileNotFoundError:
                logger.info('No token file \'{}\' found on cache dir'.format(self.token_cache_file))
            except PermissionError:
                logger.error('Cannot read token file \'{}\' from cache, please check permissions'.format(self.token_cache_file))
                self.store_token = False
        else:
            # Cache dir doesn't exists create it
            try:
                logger.debug('Creating cache dir \'{}\''.format(os.path.dirname(self.token_cache_file)))
                os.mkdir(os.path.dirname(self.token_cache_file), mode=0o700);
            except PermissionError:
                logger.error('Cannot create cache dir \'{}\' to store token, please check permissions'.format(os.path.dirname(self.token_cache_file)))
                self.store_token = False

        # If token still none try to get username and password from environment
        if self.lesspass_token == None:
            self.lesspass_user = os.environ.get('LESSPASS_USER')
            if self.lesspass_user == None:
                sys.exit('You must configure LESSPASS_USER environment variable')
            self.lesspass_pass = os.environ.get('LESSPASS_PASS')
            if self.lesspass_pass == None:
                sys.exit('You must configure LESSPASS_PASS environment variable')

config = Config()
