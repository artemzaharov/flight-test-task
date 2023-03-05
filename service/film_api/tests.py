from django.test import TestCase
from film_api.models import *
from django.db import IntegrityError
from film_api.serializers import *
import json
from film_api.tools import *
from film_api.scoring import *
import io
from django.core.files import File


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
    
    def test_content_serializer_with_file_works(self):
        #arragne 
        content = Content()
        content.name = "name"
        content.score = 123
        content.metadata = "{}"
        content.save()
        content_file = ContentFile()
        content_file.contentFK = content
        content_file.file = File(io.StringIO("Some text"), "test file")
        content_file.fileType = ContentFile.FileType.TEXT
        content_file.save()
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
        true_data = '''{"id": %d, "name": "channel name", "childs": [{"id": %d, "name": "subchannel name", "childs": [{"id": %d, "name": "content name", "metadata": "{}", "score": 123, "file": null}]}]}'''%(channel.id, subchannel.id, content.id)
                
        #act
        serializer = ChannelInTreeSerialier(channel)
        data  = serializer.data

        #assert
        self.assertIsNotNone(data)
        self.assertEqual(true_data, json.dumps(data))
    
    def test_serialize_all_channels(self):
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
        forest = get_channel_forest()
        true_data = '''{"channels": [{"id": %d, "name": "channel name", "childs": [{"id": %d, "name": "subchannel name", "childs": [{"id": %d, "name": "content name", "metadata": "{}", "score": 123, "file": null}]}]}]}'''%(channel.id, subchannel.id, content.id)

        #act
        data = ForestSerializer(forest).data

        #assert
        
        self.assertIsNotNone(data)
        self.assertEqual(true_data, json.dumps(data))

class ScoringTests(TestCase):

    def test_simple_case(self):
        #arrange 
        true_score = 123.0
        content = Content(name="test", score=true_score)
        content.save()
        channel = Channel(name="test channel")
        channel.save()
        rel = ContentRel(contentFK=content, parentFK=channel)
        rel.save()
        
        #act
        score = compute_score_for_channel(channel)

        #assert
        self.assertEqual(true_score, score)

    def test_mean_compute_rights(self):
        #arrange 
        true_score = 2
        content = Content(name="test", score=1)
        content.save()
        content2 = Content(name="test2", score=2)
        content2.save()
        content3 = Content(name="test3", score=3)
        content3.save()
        channel = Channel(name="test channel")
        channel.save()
        rel = ContentRel(contentFK=content, parentFK=channel)
        rel.save()
        rel2 = ContentRel(contentFK=content2, parentFK=channel)
        rel2.save()
        rel3 = ContentRel(contentFK=content3, parentFK=channel)
        rel3.save()

        #act
        score = compute_score_for_channel(channel)

        #assert
        self.assertEqual(true_score, score)

    def test_recursive_compute_rights(self):
        #arrange 
        true_score = 11
        content = Content(name="test", score=1)
        content.save()
        content2 = Content(name="test2", score=2)
        content2.save()
        content3 = Content(name="test3", score=3)
        content3.save()
        content4 = Content(name="test", score=10)
        content4.save()
        content5 = Content(name="test2", score=20)
        content5.save()
        content6 = Content(name="test3", score=30)
        content6.save()
        channel = Channel(name="test channel1")
        channel.save()
        channel2 = Channel(name="test channel2")
        channel2.save()
        channel3 = Channel(name="test channel root")
        channel3.save()

        rel = ContentRel(contentFK=content, parentFK=channel)
        rel.save()
        rel2 = ContentRel(contentFK=content2, parentFK=channel)
        rel2.save()
        rel3 = ContentRel(contentFK=content3, parentFK=channel)
        rel3.save()

        rel4 = ContentRel(contentFK=content4, parentFK=channel2)
        rel4.save()
        rel5 = ContentRel(contentFK=content5, parentFK=channel2)
        rel5.save()
        rel6 = ContentRel(contentFK=content6, parentFK=channel2)
        rel6.save()

        rel7 = ParentChannelRel(channelFK=channel, parentFK=channel3)
        rel7.save()
        rel8 = ParentChannelRel(channelFK=channel2, parentFK=channel3)
        rel8.save()

        #act
        score = compute_score_for_channel(channel3)

        #assert
        self.assertEqual(true_score, score)

    
