import sys
import os
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv
import pandas as pd
from colorama import Fore

# Paste API credentials here
api_id = 2362365435
api_hash = '406b124a883756fefsg24g24g'
phone = '+76668887777'


class bcolors:
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'


def banner():
    if sys.platform.lower() == "win32":
        os.system('color')

    return print(f'''================
{bcolors.RED}TELEGRAM SCRAPER{bcolors.ENDC}
================''')


def connect_client():
    try:
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone)
            client.sign_in(phone, input('Enter the code: '))
            connect_client()
        else:
            return print('Telegram API authorized')
    except:
        return print('API Credentials are invalid. Please try again')


def list_groups():
    chats = []
    last_date = None
    chunk_size = 200
    groups = []

    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue

    return groups


def target_group(groups):
    print(f'{bcolors.YELLOW}Choose a group to scrape members from:{bcolors.ENDC}')
    i = 0
    for g in groups:
        print(str(i) + '- ' + g.title)
        i += 1

    g_index = input("Enter a Number: ")
    target_group = groups[int(g_index)]

    return target_group


def get_members(target_group):
    print('Fetching Members...')
    try:
        all_participants = client.get_participants(
            target_group, aggressive=True)
    except Exception as e:
        return print(e)

    return all_participants


def data_to_csv(all_participants, target_group):
    print('Saving In file...')

    with open("members.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=";", lineterminator="\n")
        writer.writerow(['username', 'user id', 'access hash',
                        'name', 'group', 'group id'])
        for user in all_participants:
            if user.username:
                username = user.username
            else:
                username = ""
            if user.first_name:
                first_name = user.first_name
            else:
                first_name = ""
            if user.last_name:
                last_name = user.last_name
            else:
                last_name = ""
            name = (first_name + ' ' + last_name).strip()
            writer.writerow([username, user.id, user.access_hash,
                            name, target_group.title, target_group.id])
    print('Members scraped successfully.')


def data_to_xlsx(all_participants, target_group):
    print('Saving In file...')

    username_list = []
    name_list = []
    id_list = []
    hash_list = []
    group_list = []
    group_id_list = []

    count = 1
    for user in all_participants:
        if user.username:
            username = user.username
        else:
            username = ""
        if user.first_name:
            first_name = user.first_name
        else:
            first_name = ""
        if user.last_name:
            last_name = user.last_name
        else:
            last_name = ""
        name = (first_name + ' ' + last_name).strip()
        username_list.append(username)
        name_list.append(name)
        id_list.append(user.id)
        hash_list.append(user.access_hash)
        group_list.append(target_group.title)
        group_id_list.append(target_group.id)

        print(str(count) + ' users scraped')
        count += 1

    df = pd.DataFrame({'username': username_list, 'name': name_list, 'user id': id_list,
                       'hash': hash_list, 'group': group_list, 'group id': group_id_list})
    df.to_excel(f'members.xlsx', encoding='utf-8',
                index=False, header=True)

    return print(f'{bcolors.YELLOW}All done!{bcolors.ENDC}')


if __name__ == "__main__":
    banner()

    client = TelegramClient(phone, api_id, api_hash)

    connect_client()
    group = target_group(list_groups())
    all_participants = get_members(group)
    data_to_xlsx(all_participants, group)
    # data_to_csv(all_participants, group)
