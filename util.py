from datetime import datetime

import settings


def time_format(time_sec):
    sec = time_sec % 60
    min = time_sec / 60
    return '{}:{}'.format(int(min), sec)


def last_number_in_link(link):
    m_link_data = link.split('/')
    result_link = ''.join(item for item in m_link_data[-1] if item.isdigit())
    return int(result_link)


def read_bot_users(filename):
    file = open(filename, 'r')
    f_data = file.readlines()
    f_twitch_names = []
    f_osu_ids = []
    for lines in f_data:
        f_twitch_names.append(lines.split(" ")[0].lower())
        f_osu_ids.append(int(lines.split(" ")[1]))
    file.close()
    return f_twitch_names, f_osu_ids


def user_data_list_from_channel_name(channel):
    for data in settings.USER_DATA:
        if data[1] == channel:
            return data

def get_date():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string
