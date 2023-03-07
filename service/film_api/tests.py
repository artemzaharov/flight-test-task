from django.test import TestCase
from film_api.models import *
from django.db import IntegrityError
from film_api.serializers import *
import json
from film_api.tools import *
from film_api.scoring import *
import io
from django.core.files import File
from django.core.files.images import ImageFile
from io import StringIO 

def create_empty_content():
    empty_content = Content(name=CONTENT_EMPTY_CONTENT_NAME)
    empty_content.metadata={'text':CONTENT_EMPTY_CONTENT_TEXT}
    empty_content.save()

def fill_channel_fields(channel):
    file = StringIO("test")
    channel.language = 'ru'
    channel.image = ImageFile(file, "test.jpg")
    pass

class ConstraintsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_empty_content()
    
    def test_no_reversing_rel_in_channel(self):
        #arrange 

        channel = Channel()
        channel.name = "test"
        fill_channel_fields(channel)
        channel.save()

        #act
        try:
            channel.parentChannels.add(channel)
            channel.save()
            isRaised = False
        except ValidationError:
            isRaised = True
        
        #assert 
        self.assertTrue(isRaised)
        
    def test_no_duplicate_rel_in_channel(self):
        #arrange 
        file = StringIO("test")
        channel1 = Channel()
        channel1.name = "test1"
        fill_channel_fields(channel1)
        channel1.save()

        channel2 = Channel()
        channel2.name = "test2"
        fill_channel_fields(channel2)
        channel2.save()

        channel2.parentChannels.add(channel1)
        channel2.save()
        
        channel2.parentChannels.add(channel1)
        
        #act
        channel2.save()

        #assert 
        self.assertTrue(channel2.parentChannels.count()  == 1)
    
    def test_no_cycling_rel_in_channel(self):
        #arrange 
        file = StringIO("test")
        channel1 = Channel()
        channel1.name = "test"
        fill_channel_fields(channel1)
        channel1.save()

        channel2 = Channel()
        channel2.name = "test"
        fill_channel_fields(channel2)
        channel2.save()

        channel1.parentChannels.add(channel2)

        channel1.save()
        

        #act
        try:
            channel2.parentChannels.add(channel1)
            channel2.save()
            isRaised = False
        except ValidationError:
            isRaised = True
        
        #assert 
        self.assertTrue(isRaised)
    
    def test_no_long_cycling_rel_in_channel(self):
        #arrange 
        file = StringIO("test")
        channel1 = Channel()
        channel1.name = "test"
        fill_channel_fields(channel1)
        channel1.save()

        channel2 = Channel()
        channel2.name = "test"
        fill_channel_fields(channel2)
        channel2.save()
        channel3 = Channel()
        channel3.name = "test"
        fill_channel_fields(channel3)
        channel3.save()

        channel2.parentChannels.add(channel1)
        channel2.save()
        channel3.parentChannels.add(channel2)
        channel3.save()
        #act
        try:
            channel1.parentChannels.add(channel3)
            channel1.save()
            isRaised = False
        except ValidationError:
            isRaised = True
        
        #assert 
        self.assertTrue(isRaised)
    
    def test_content_count_computes_right(self):
        #act
        file = StringIO("test")
        ch = Channel(name='test')
        fill_channel_fields(ch)
        ch.save()
        content = Content(name="content")
        content.save()
        content.parentChannels.add(ch)
        #arrange
        content.save()
        ch.refresh_from_db()
        #assert
        self.assertEqual(1, ch.content_count)


class SerializersTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_empty_content()
    

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
        file = StringIO("test")
        content = Content()
        content.name = "content name"
        content.score = 123
        content.metadata = "{}"
        content.save()
        channel = Channel()
        channel.name = "channel name"
        fill_channel_fields(channel)

        channel.save()
        subchannel = Channel()
        subchannel.name = "subchannel name"
        fill_channel_fields(subchannel)
        subchannel.save()
        subchannel.parentChannels.add(channel)
        subchannel.save()
        content.parentChannels.add(subchannel)
        content.save()
        true_data = '''{"id": %d, "name": "channel name", "language": "ru", "image": "%s", "childs": [{"id": %d, "name": "subchannel name", "language": "ru", "image": "%s", "childs": [{"id": %d, "name": "content name", "metadata": "{}", "score": 123, "file": null}]}]}'''%(channel.id, channel.image.url, subchannel.id,subchannel.image.url, content.id)
                
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
        fill_channel_fields(channel)
        channel.save()
        subchannel = Channel()
        subchannel.name = "subchannel name"
        fill_channel_fields(subchannel)
        subchannel.save()
        subchannel.parentChannels.add(channel)
        subchannel.save()
        content.parentChannels.add(subchannel)
        content.save()
        forest = get_channel_forest()
        true_data = '''{"channels": [{"id": %d, "name": "channel name", "language": "ru", "image": "%s", "childs": [{"id": %d, "name": "subchannel name", "language": "ru", "image": "%s", "childs": [{"id": %d, "name": "content name", "metadata": "{}", "score": 123, "file": null}]}]}]}'''%(channel.id, channel.image.url, subchannel.id, subchannel.image.url, content.id)

        #act
        data = ForestSerializer(forest).data

        #assert
        self.assertIsNotNone(data)
        self.assertEqual(true_data, json.dumps(data))

class ScoringTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_empty_content()
    

    def test_simple_case(self):
        #arrange 
        true_score = 123.0
        content = Content(name="test", score=true_score)
        content.save()
        channel = Channel(name="test channel")
        fill_channel_fields(channel)
        channel.save()
        content.parentChannels.add(channel)
        content.save()
        
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
        fill_channel_fields(channel)
        channel.save()
        content.parentChannels.add(channel)
        content.save()
        content2.parentChannels.add(channel)
        content2.save()
        content3.parentChannels.add(channel)
        content3.save()

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
        fill_channel_fields(channel)
        channel.save()
        channel2 = Channel(name="test channel2")
        fill_channel_fields(channel2)
        channel2.save()
        channel3 = Channel(name="test channel root")
        fill_channel_fields(channel3)
        channel3.save()

        content.parentChannels.add(channel)
        content.save()
        content2.parentChannels.add(channel)
        content2.save()
        content3.parentChannels.add(channel)
        content3.save()

        content4.parentChannels.add(channel2)
        content4.save()
        content5.parentChannels.add(channel2)
        content5.save()
        content6.parentChannels.add(channel2)
        content6.save()

        channel.parentChannels.add(channel3)
        channel.save()
        channel2.parentChannels.add(channel3)
        channel2.save()

        #act
        score = compute_score_for_channel(channel3)

        #assert
        self.assertEqual(true_score, score)

    
