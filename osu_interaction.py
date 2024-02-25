from ossapi import Ossapi, Scope, UserLookupKey, GameMode, RankingType, ScoreType

import LOGGER
import db_interaction
import util
import settings

client_id = settings.OSU_CLIENT_ID
client_secret = settings.OSU_CLIENT_SECRET
callback_url = 'http://localhost:3914/'
scopes = [Scope.PUBLIC, Scope.CHAT_WRITE]


# create a new client at https://osu.ppy.sh/home/account/edit#oauth


# see docs for full list of endpoints
def send_map_msg(type, id, user_data, mode):  # 1: type 0 -map, 1 - set, 2: set/map id 3: user_list    (map_msg)

    api = Ossapi(client_id, client_secret, callback_url, scopes=scopes)

    if type == 0:
        map_resp = api.beatmap(beatmap_id=int(id))
        map_link = 'https://osu.ppy.sh/beatmapsets/' + str(map_resp.beatmapset().id) + '#osu/' + id
        pm_message = f'{mode}: [{map_link}  {map_resp.beatmapset().artist} - {map_resp.beatmapset().title} [{map_resp.version}]] {util.time_format(int(map_resp.total_length))} ★ {map_resp.difficulty_rating}  ♫ {map_resp.bpm} AR{map_resp.ar} CS{map_resp.cs} OD{map_resp.accuracy} {map_resp.beatmapset().status.name.lower()}'
        api.send_pm(user_data[2], pm_message)
        LOGGER.log("REQUEST: user: " + user_data[1] + " data: " + pm_message)

    elif type == 1:
        map_resp = api.beatmapset(beatmapset_id=int(id))
        mode = map_resp.beatmaps[0].mode.value
        map_link = 'https://osu.ppy.sh/beatmapsets/' + str(map_resp.id)
        pm_message = f'{mode}: [{map_link}  {map_resp.artist} - {map_resp.title}]'
        api.send_pm(user_data[2], pm_message)
        LOGGER.log(f'REQUEST: user: {user_data[1]} data: {pm_message}')
    else:
        LOGGER.log(f'REQUEST: user: {user_data[1]} ERROR DURING ANALYZE!  DATA: {type} {id} {user_data} {mode}')


def get_last_played_map(channel_name):
    user_data = util.user_data_list_from_channel_name(channel_name)
    api = Ossapi(client_id, client_secret, callback_url, scopes=scopes)
    api_resp = api.user_scores(user_id=user_data[2], type=ScoreType.RECENT, include_fails=True)
    result = api_resp[0]
    message = f'{result.beatmapset.artist} - {result.beatmapset.title} [{result.beatmap.version}]  ★{result.beatmap.difficulty_rating} {result.beatmapset.status.name.lower()} {result.beatmap.url}'
    LOGGER.log(f'RS: user: {user_data[1]} data: {message}')
    return message
