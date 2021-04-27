# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020-2021 Óscar García Amor <ogarcia@connectical.com>
#
# Distributed under terms of the GNU GPLv3 license.

from lpacli.config import config

import logging
import requests

logger = logging.getLogger(__name__)

class LessPassApiClient:
    def __init__(self, **kwargs):
        self.lesspass_token = kwargs.get('lesspass_token', config.lesspass_token)
        self.lesspass_host = kwargs.get('lesspass_host', config.lesspass_host)
        self.lesspass_user = kwargs.get('lesspass_user', config.lesspass_user)
        self.lesspass_pass = kwargs.get('lesspass_pass', config.lesspass_pass)

    def request(self, method, uri, **kwargs):
        if self.lesspass_token is not None:
            headers = kwargs.get('headers', {})
            headers['authorization'] = 'Bearer {}'.format(self.lesspass_token)
            kwargs['headers'] = headers

        url = requests.compat.urljoin(self.lesspass_host, uri)
        logger.debug('Querying {} to {}'.format(method, url))
        return requests.request(method, url, **kwargs)

    def get_token(self):
        json = {'email': self.lesspass_user, 'password': self.lesspass_pass}
        return self.request('POST', 'auth/jwt/create/', json=json)

    def update_token(self):
        json = {'refresh': self.lesspass_token}
        return self.request('POST', 'auth/jwt/refresh/', json=json)

    def get_passwords(self):
        return self.request('GET', 'passwords/')

