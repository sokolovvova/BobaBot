import LOGGER
import util
import LOGGER
from util import last_number_in_link
import osu_interaction


def osu_msg(type, id, user_data, mode):   # 1: type 0 -map, 1 - set, 2: set/map id 3: user_list 4:mode
    osu_interaction.send_map_msg(type, id, user_data, mode)
    return


async def analyze_msg(msg, channel_name, author_name):
    LOGGER.msg_log(msg,channel_name,author_name)
    user_data = util.user_data_list_from_channel_name(channel_name)
    res = "error"
    if user_data[3] == 1:
        data_list = msg.split(" ")
        for data in data_list:
            res = await check_btm_link(data, user_data)
        return res
    return res


async def check_btm_link(msg, user_data):
    response = None
    link_type = None
    map_mode = None
    map_id = None
    beatmap_set_id = None
    if "/s/" in msg:
        msg = msg.replace("/s/", "/beatmapset/")

    if "osu.ppy.sh" in msg:
        if "#mania" in msg:
            map_mode = "mania"
            link_type = "map"
            map_id = last_number_in_link(msg)
        elif "#fruits" in msg:
            map_mode = "fruits"
            link_type = "map"
            map_id = last_number_in_link(msg)
        elif "#taiko" in msg:
            map_mode = "taiko"
            link_type = "map"
            map_id = last_number_in_link(msg)
        elif "#osu" in msg:
            map_mode = "osu"
            link_type = "map"
            map_id = last_number_in_link(msg)
        else:
            if "beatmapset" in msg:
                beatmap_set_id = last_number_in_link(msg)
                link_type = "beatmap_set"

    if link_type != None:
        if beatmap_set_id != None:
            osu_msg(1, str(beatmap_set_id), user_data, None)
            response = "Thanks for beatmapset request!"
        elif map_id != None:
            osu_msg(0, str(map_id), user_data, map_mode)
            response = "Thanks for beatmap request!"
        else:
            response = "error"
    else:
        response = "error"
    if response != 'error':
        LOGGER.log(f'   {msg} response: [{response}]')
    return response
