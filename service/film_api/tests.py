from django.test import TestCase
from film_api.models import *
from django.db import IntegrityError
from film_api.serializers import *

class ConstraintsTests(TestCase):
    def test_no_reversing_rel_in_channel(self):
        #arrange 
        channel = Channel()
        channel.name = "test"
        channel.save()

        channelRel = ParentChannelRel()
        channelRel.channelFK = channel
        channelRel.parentFK = channel

        #act
        try:
            channelRel.save()
            isRaised = False
        except ValidationError:
            isRaised = True
        
        #assert 
        self.assertTrue(isRaised)
        
    def test_no_duplicate_rel_in_channel(self):
        #arrange 
        channel1 = Channel()
        channel1.name = "test"
        channel1.save()

        channel2 = Channel()
        channel2.name = "test"
        channel2.save()

        channelRel1 = ParentChannelRel()
        channelRel1.channelFK = channel1
        channelRel1.parentFK = channel2
        channelRel1.save()

        channelRel2 = ParentChannelRel()
        channelRel2.channelFK = channel1
        channelRel2.parentFK = channel2

        #act
        try:
            channelRel2.save()
            isRaised = False
        except ValidationError:
            isRaised = True
        
        #assert 
        self.assertTrue(isRaised)
    
    def test_no_cycling_rel_in_channel(self):
        #arrange 
        channel1 = Channel()
        channel1.name = "test"
        channel1.save()

        channel2 = Channel()
        channel2.name = "test"
        channel2.save()

        channelRel1 = ParentChannelRel()
        channelRel1.channelFK = channel1
        channelRel1.parentFK = channel2
        channelRel1.save()

        channelRel2 = ParentChannelRel()
        channelRel2.channelFK = channel2
        channelRel2.parentFK = channel1

        #act
        try:
            channelRel2.save()
            isRaised = False
        except ValidationError:
            isRaised = True
        
        #assert 
        self.assertTrue(isRaised)


class SerializersTest(TestCase):

    def test_content_serializer_works(self):
        #arragne 
        content = Content()
        content.name = "name"
        content.score = 123
        content.metadata = "{}"
        content.save()
        # contentFile = ContentFile()

        #act
        serializer = ContentSerializer(content)
        data = serializer.data

        #assert
        self.assertIsNotNone(data)
    
    def test_channel_serialier_works(self):
        #arrange
        content = Content()
        content.name = "content name"
        content.score = 123
        content.metadata = "{}"
        content.save()
        channel = Channel()
        channel.name = "channel name"
        channel.save()
        subchannel = Channel()
        subchannel.name = "subchannel name"
        subchannel.save()
        subchannelRel = ParentChannelRel()
        subchannelRel.channelFK = subchannel
        subchannelRel.parentFK = channel
        subchannelRel.save()
        contentRel = ContentRel()
        contentRel.contentFK = content
        contentRel.parentFK = subchannel
        contentRel.save()

        subchannel.content_childs = [rel.contentFK for rel in channel.channel_contents.get_queryset()]
        channel.channel_childs = [rel.channelFK for rel in channel.channel_subchannels.get_queryset()]
        
        #act
        serializer = ChannelInTreeSerialier(channel)
        data  = serializer.data

        #assert
        self.assertIsNotNone(data)