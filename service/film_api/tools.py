
from film_api.support_types import *
from film_api.models import *

def channel_to_content_childs(channel):
    return channel.child_contents.all()

def channel_to_subchannels(channel):
    return  channel.child_channels.all()

def get_channel_forest():
    return ChannelForest(Channel.objects.filter(parents_count=0))

def recursive_query_all_descendans_channels(channel):
    if channel.child_contents.count() > 0:
        return [channel]
    ret = [channel]
    for subchannel in channel.child_channels.all():
        ret.extend(recursive_query_all_descendans_channels(subchannel))
    return ret