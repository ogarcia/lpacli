# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020-2021 Óscar García Amor <ogarcia@connectical.com>
#
# Distributed under terms of the GNU GPLv3 license.

from lpacli.api.lesspassapiclient import LessPassApiClient
from lpacli.config import config

import logging
import os
import sys

logger = logging.getLogger(__name__)

class Login:
    def __init__(self, **kwargs):
        self.token_cache_file = kwargs.get('token_cache_file', config.token_cache_file)
        self.store_token = kwargs.get('store_token', config.store_token)
        self.lesspass_token = kwargs.get('lesspass_token', config.lesspass_token)
        self.lesspass_api_client = LessPassApiClient()

    def _store_token(self, token):
        try:
            with open(self.token_cache_file, 'w') as writer:
                writer.write(token)
            os.chmod(self.token_cache_file, 0o600)
        except PermissionError:
            logger.error('Cannot write token file \'{}\' from cache, please check permissions'.format(self.token_cache_file))

    def perform_login(self):
        if self.lesspass_token == None:
            logger.debug('Asking for new token')
            response = self.lesspass_api_client.get_token()
        else:
            logger.debug('Asking for token refresh')
            response = self.lesspass_api_client.update_token()
        if response.status_code == 200 or response.status_code == 201:
            response_json = response.json()
            config.lesspass_token = response_json.get('refresh', response_json.get('access', ''))
            logger.debug('Response: {}'.format(response_json))
            logger.debug('Stored token: {}'.format(config.lesspass_token))
            if self.store_token:
                self._store_token(config.lesspass_token)
        else:
            logger.debug('API response: {}'.format(response.text))
            if self.lesspass_token == None:
                sys.exit('Cannot perform login, API response code: {}'.format(response.status_code))
            else:
                if self.store_token:
                    self._store_token('')
                sys.exit('Your token has expired, please try login again with username and password environment variables')
