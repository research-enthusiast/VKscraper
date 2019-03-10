# -*- coding: utf-8 -*-

import argparse
import vk_api
import json
import sqlite3
import csv

parser = argparse.ArgumentParser(
        description="Input app id and client_secret"
        )
parser.add_argument('-um', '--user_auth', 
                    help='Authorize by login and password if 1 or by app id and client secret if 0', 
                    default=1, type=int)
parser.add_argument('-ai', '--app_id', help='VK application id number', type=int)
parser.add_argument('-cs', '--client_secret', help='VK application client secret number')
parser.add_argument('-l', '--login', help='VK user login')
parser.add_argument('-p', '--password', help='VK user password')
args = parser.parse_args()

def auth(args):
    if not args.user_auth:
        vk_sess = vk_api.VkApi(app_id=args.app_id, client_secret=args.client_secret)
    else:
        vk_sess = vk_api.VkApi(args.login, args.password)

    try:
        if not args.user_auth:
            vk_sess.server_auth()
        else:
            vk_sess.auth()
    except vk_api.AuthError as err_msg:
        print(err_msg)

    return vk_sess

vk_sess = auth(args)
vk = vk_sess.get_api()
