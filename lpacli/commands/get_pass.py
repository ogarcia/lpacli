# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020-2021 Óscar García Amor <ogarcia@connectical.com>
#
# Distributed under terms of the GNU GPLv3 license.

from lpacli.login import Login
from lpacli.api.lesspassapiclient import LessPassApiClient

from lesspass.password import generate_password

import os
import sys

def get_pass(args):
    # Perform login to API
    lesspass_login = Login()
    lesspass_login.perform_login()

    # Get passwords list
    lesspass_api_client = LessPassApiClient()
    response = lesspass_api_client.get_passwords()

    if response.status_code == 200:
        sites = response.json().get('results')
        # List sites or get site password options
        if args.site == 'ls':
            for site in sites:
                sys.stdout.write('{}\n'.format(site.get('site')))
        else:
            site_data = None
            for site in sites:
                if site.get('site') == args.site:
                    site_data = site
                    break
            if site_data == None:
                sys.stdout.write('Cannot find any data of site \'{}\'\n'.format(args.site))
            else:
                lesspass_masterpassword = os.environ.get('LESSPASS_MASTERPASS')
                site_data['digits'] = site_data.get('numbers')
                if lesspass_masterpassword == None or args.settings:
                    # Print options
                    sys.stdout.write('Site: {}\n'.format(site_data.get('site')))
                    sys.stdout.write('Login: {}\n'.format(site_data.get('login')))
                    sys.stdout.write('Lowercase: {}\n'.format(site_data.get('lowercase')))
                    sys.stdout.write('Uppercase: {}\n'.format(site_data.get('uppercase')))
                    sys.stdout.write('Digits: {}\n'.format(site_data.get('digits')))
                    sys.stdout.write('Symbols: {}\n'.format(site_data.get('symbols')))
                    sys.stdout.write('Length: {}\n'.format(site_data.get('length')))
                    sys.stdout.write('Counter: {}\n'.format(site_data.get('counter')))
                else:
                    # Print password
                    sys.stdout.write('{}\n'.format(generate_password(site_data, lesspass_masterpassword)))
