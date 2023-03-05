from film_api.models import *
from film_api.tools import *
import math as m


def compute_score_for_channel_rec(channel, cache):
    if channel.id in cache:
        return cache[channel.id]
    content_childs = channel_to_content_childs(channel)
    if len(content_childs) > 0:
        result = sum([child.score for child in content_childs]) / len(content_childs)
    else:
        subchannels  = channel_to_subchannels(channel)
        result = sum([compute_score_for_channel_rec(child, cache) for child in subchannels]) / len(subchannels)
    cache[channel.id] = result
    return result

def compute_score_for_channel(channel):
    return compute_score_for_channel_rec(channel, {})


def compute_score_for_all_channels():
    forest = get_channel_forest()
    channels_score_map = {}
    [compute_score_for_channel_rec(root, channels_score_map) for root in forest.channels]
    score_with_names = [(key, Channel.objects.get(id=key).name, channels_score_map[key]) for key in channels_score_map]
    return score_with_names

def get_score_report():
    score = compute_score_for_all_channels()
    score = [(str(el[0]), el[1].replace(";", ","), str(el[2])) for el in score]
    file_content = "id;name;score\n" + "\n".join([";".join(el) for el in score])
    return file_content