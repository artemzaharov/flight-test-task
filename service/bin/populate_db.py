import os
from os import path as p
from random import randint
import django
import random
os.environ['DJANGO_SETTINGS_MODULE'] = 'service.settings'
django.setup()
from film_api.models  import *
from django.core.files import File
from django.core.files.images import ImageFile
import io

test_files_dir = "bin/data"
test_files = [
    (ContentFile.FileType.TEXT, p.join(test_files_dir, "text.txt")),
    (ContentFile.FileType.PDF, p.join(test_files_dir, "pdf.pdf")),
    (ContentFile.FileType.VIDEO, p.join(test_files_dir, "video.mkv")),
]

test_langs = ['ru', 'en', 'cn']
test_channel_image_path = test_files_dir+ "/test_channel_image.jpg"

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
    

    with open(test_channel_image_path, 'rb') as f:
        channel_image = io.BytesIO(f.read())


    for i in range(3):
        channel = Channel()
        channel.name = random_element(channels)
        channel.language = random_element(test_langs)
        channel.image = ImageFile(channel_image, f"{channel.name}.jpg")
        channel.save()
        for j in range(5):
            subchannel = Channel()
            subchannel.name = random_element(subchannels)
            subchannel.language = random_element(test_langs)
            channel_image.seek(0)
            subchannel.image = ImageFile(channel_image, f"{subchannel.name}.jpg")
            subchannel.save()
            subchannel.parentChannels.add(channel)
            subchannel.save()
            for k in range(2):
                content = Content()
                content.name = random_element(tv_shows+films)
                content.metadata = "{}"
                content.score = randint(0, 10)
                content.save()
                test_file = random_element(test_files)
                contentFile = ContentFile()
                contentFile.fileType = test_file[0]
                with open(test_file[1], 'rb') as f:
                    contentFile.file = File(io.BytesIO(f.read()), test_file[1])
                contentFile.contentFK = content
                contentFile.save()
                content.parentChannels.add(subchannel)
                content.save()
# set1()

set2()
