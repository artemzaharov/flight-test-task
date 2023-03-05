import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'service.settings'
import django
django.setup()


from film_api.models  import *

for i in range(3):
    channel = Channel()
    channel.name = f"test channel {i}"
    channel.save()
    for j in range(5):
        subchannel = Channel()
        subchannel.name = f"test subchannel {j}"
        subchannel.save()
        subchannelRel = ParentChannelRel()
        subchannelRel.channelFK = subchannel
        subchannelRel.parentFK = channel
        subchannelRel.save()
        for k in range(2):
            content = Content()
            content.name = f"test content {k}"
            content.metadata = "{}"
            content.save()
            contentRel = ContentRel()
            contentRel.contentFK = content
            contentRel.parentFK = subchannel
            contentRel.save()



