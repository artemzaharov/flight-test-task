
from film_api.support_types import *
from film_api.models import *

def channel_to_content_childs(channel):
    return [rel.contentFK for rel in channel.channel_contents.get_queryset()]

def channel_to_subchannels(channel):
    return  [rel.channelFK for rel in channel.channel_subchannels.get_queryset()]

def get_channel_forest():
    return ChannelForest(Channel.objects.filter(parents_count=0))