import os
from random import randint
import django
import random
os.environ['DJANGO_SETTINGS_MODULE'] = 'service.settings'
django.setup()
from film_api.models  import *



def set1():
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

def random_element(list):
        return list[randint(0, len(list)-1)]

def set2():
    channels = ["Action", "Adventure", "Comedy", "Crime", "Drama", "Fantasy", "Horror", "Mystery", "Romance", "Science Fiction", "Thriller", "Western"]
    subchannels = ["Comedy_drama",  "Romantic_drama", "Romantic_thriller", "Romantic_fantasy", "Romantic_horror",
                    "Romantic_mystery", "Romantic_science_fiction", "Romantic_western", "Comedy_horror", "Comedy_mystery",
                    "Comedy_science_fiction", "Comedy_western", "Drama_horror", "Drama_mystery", "Drama_science_fiction",  "Fantasy_thriller", 
                    "Fantasy_western", "Thriller_comedy", "Thriller_drama", "Thriller_fantasy", "Thriller_horror", 
                    "Thriller_mystery", "Thriller_romance", "Thriller_science_fiction", "Thriller_western"]
    tv_shows = ["Breaking Bad", "Game of Thrones", "The Sopranos", "Friends", "The Office", "Stranger Things", "The Crown", "The Handmaid's Tale", "Black Mirror", "Narcos", "Mad Men", "The Big Bang Theory"]

    films = ["The Godfather", "The Shawshank Redemption", "The Dark Knight", "Forrest Gump", "Pulp Fiction", "The Matrix", "The Silence of the Lambs", "Jurassic Park", "Star Wars", "The Lord of the Rings", "Indiana Jones", "Back to the Future"]
    


    for i in range(3):
        channel = Channel()
        channel.name = random_element(channels)
        channel.save()
        for j in range(5):
            subchannel = Channel()
            subchannel.name = random_element(subchannels)
            subchannel.save()
            subchannelRel = ParentChannelRel()
            subchannelRel.channelFK = subchannel
            subchannelRel.parentFK = channel
            subchannelRel.save()
            for k in range(2):
                content = Content()
            content.name = random_element(tv_shows+films)
            content.metadata = "{}"
            content.score = randint(0, 10)
            content.save()
            contentRel = ContentRel()
            contentRel.contentFK = content
            contentRel.parentFK = subchannel
            contentRel.save()
# set1()

set2()
