from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv

api_id = 27434827
api_hash = '406b124a883756da21f75b7ee62d9227'
phone = '+79817097969'


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
    print('Choose a group to scrape members from:')
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


if __name__ == "__main__":

    client = TelegramClient(phone, api_id, api_hash)

    connect_client()
    group = target_group(list_groups())
    all_participants = get_members(group)
    data_to_csv(all_participants, group)
