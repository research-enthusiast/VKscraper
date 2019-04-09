# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from vkapifields import VKFIELDS
from vk_api.audio import VkAudio
import vk_api
import json
import sqlite3
import csv
import os
import sys

flds = VKFIELDS()

parser = ArgumentParser(description="Input app id and client_secret")
parser.add_argument('-um', '--user_auth', 
                    help='Authorize by login and password if 1 or by app id and client secret if 0', 
                    default=1, type=int)
parser.add_argument('-ai', '--app_id', help='VK application id number', type=int)
parser.add_argument('-cs', '--client_secret', help='VK application client secret number')
parser.add_argument('-l', '--login', help='VK user login')
parser.add_argument('-p', '--password', help='VK user password')
parser.add_argument('-om', '--operation_mode', 
                    help='Working mode. p - extract all infomation from users pages specified \
                    in csv list of users IDs, r - replace all user domain names to IDs in csv \
                    file, s - search users by specified criteria')
parser.add_argument('-lst', '--users_list', help='VK users csv file')
parser.add_argument('-out', '--out_users_data', help='csv file containing all parsed users',
                    default='parsed_users.csv')
args = parser.parse_args()

def create_file(f, lst):
    if not os.path.exists(f):
        print(f + " created")
        with open(f, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, lineterminator='\n', delimiter = '|')
            writer.writerow(lst)

def create_users_files(base_dir, uid):
    """
    Create folder and respective csv file for the new user
    """
    create_dir = os.path.join(base_dir, uid)
    if not os.path.exists(create_dir):
        os.mkdir(create_dir)

    # Crete file for user's audio
    audio_file = os.path.join(create_dir, 'audio.csv')
    create_file(audio_file, flds.AUDIO_LIST)
    
    # Crete main file for all parsed profiles
    profile_file = args.out_users_data
    create_file(profile_file, flds.REQ_LIST)

def captcha_handler(cap):
    """
    Captch handler. If it is appear then copy the link to it, and input result to a console
    """
    key = input("Enter captcha {0}: ".format(cap.get_url())).strip()
    return cap.try_again(key)

def auth(args):
    """
    Auth on VK server
    """
    if not args.user_auth:
        vk_sess = vk_api.VkApi(app_id=args.app_id, 
                               client_secret=args.client_secret, 
                               captcha_handler=captcha_handler)
    else:
        vk_sess = vk_api.VkApi(args.login,
                               args.password, 
                               captcha_handler=captcha_handler)

    try:
        if not args.user_auth:
            # Auth by application
            vk_sess.server_auth()
        else:
            # Auth by VK user login and password
            vk_sess.auth()
    except vk_api.AuthError as err_msg:
        print(err_msg)

    return vk_sess

vk_sess = auth(args)

# Some user inputs checks
if args.users_list == '' or args.users_list is None:
    sys.exit("No users list file provided!")

if args.operation_mode == 'p':
    """
    Parse all information from user. 
    Personal data, wall posts, music list
    """

    # Get personal information
    base_dir = os.path.dirname(args.users_list)
    uid = '50549738' #'1304050'
    create_users_files(base_dir, uid)
    with open(args.users_list) as usrs_file:
        csv_reader = csv.reader(usrs_file)
        next(csv_reader)

    vk = vk_sess.get_api()
    resp = vk.users.get(user_ids = uid, fields = ','.join(flds.REQ_LIST))
    
    # Write to file
    users_data_write = []
    for i in flds.REQ_LIST:
        # process speicial fields which are returned as separate fields for some reason,
        # probably because of vk_api library implementation
        try:
            cval = resp[0][i]
        except:
            users_data_write.append('')
            continue

        if type(cval) == int:
            users_data_write.append(str(cval))
        elif type(cval) == list:
            s = ' ; '.join(' , '.join('{!s}={!r}'.format(key,val) for (key,val) in d.items()) for d in cval)
            users_data_write.append(s)
        elif type(cval) == dict:
            s = ' , '.join('{!s}={!r}'.format(key,val) for (key,val) in cval.items())
            users_data_write.append(s)
        else:
            users_data_write.append(cval)

    path_to_users = args.out_users_data
    with open(path_to_users, 'a', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n', delimiter='|')
        writer.writerow(users_data_write)
    
    # Get wall posts
    #tools = vk_api.VkTools(vk_sess)
    #wall = tools.get_all('wall.get', 100, {'owner_id': uid})
    
    # Get music lists
    vkaudio = VkAudio(vk_sess)
    audios_list = vkaudio.get(owner_id = 1304050)
    
    # Write to file
    path_to_audios = os.path.join(base_dir, uid, 'audio.csv')
    with open(path_to_audios, 'a', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n', delimiter = '|')
        
        for a in audios_list:
            users_audio_write = []
            for i in flds.AUDIO_LIST:
                cval = a[i]
                if type(cval) == int:
                    users_audio_write.append(str(cval))
                else:
                    users_audio_write.append(cval)
    
            writer.writerow(users_audio_write)

if args.operation_mode == 'r':
    """
    Replace all short names (domains) of user to IDs in csv file
    """
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
                raw_resp.extend(vk.users.get(user_ids = lst))
        else:
            lst = ','.join(users)
            raw_resp = vk.users.get(user_ids = lst)

    # Extract list of ID's from response list
    lst_ids = [x['id'] for x in raw_resp]
    # Save list as csv file
    with open(args.users_list[:-4] + '_ids.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(lst_ids)
