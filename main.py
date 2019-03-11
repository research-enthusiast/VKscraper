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
parser.add_argument('-om', '--operation_mode', 
                    help='Working mode. g - extract all infomation from users pages specified \
                    in csv list of users IDs, r - replace all user domain names to IDs in csv \
                    file, s - search users by specified criteria')
parser.add_argument('-lst', '--users_list', help='VK users csv file')
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

if args.operation_mode == 'r':
    raw_resp = []
    n_users = 0
    cs = 999
    with open(args.users_list) as usrs_file:
        csv_reader = csv.reader(usrs_file)
        users = next(csv_reader)
        vk = vk_sess.get_api()
        if len(users) > 999:
            # Partion list to chunks of size cs
            users_chnkd = [users[i * cs:(i + 1) * cs] for i in range((len(users) + cs - 1) // cs)]
            for ch in users_chnkd:
                lst = ','.join(ch)
                raw_resp.extend(vk.users.get(user_ids=lst))
        else:
            lst = ','.join(users)
            raw_resp = vk.users.get(user_ids=lst)

    # Extract list of ID's from response list
    lst_ids = [x['id'] for x in raw_resp]
    # Save list as csv file
    with open(args.users_list[:-4] + '_ids.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(lst_ids)
