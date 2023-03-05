from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Content(models.Model):
    score = models.IntegerField()
    name = models.CharField(max_length=200)
    metadata = models.JSONField()

class ContentFile(models.Model):
    class FieldType(models.TextChoices):
        VIDEO = "VI", _('Video file')
        PDF = "PF", _("PDF file")
        TEXT = "TX", _("Text file")

    file = models.FileField()
    fileType= models.CharField(choices=FieldType.choices, default=FieldType.VIDEO, max_length=2)
    contentFK = models.ForeignKey(Content, on_delete=models.CASCADE)

class Channel(models.Model):
    name = models.CharField(max_length=200)

#TODO запретить оба ключа на один канал.
class ParentChannelRel(models.Model):
    channelFK = models.ForeignKey(Channel, models.CASCADE, related_name="this")
    parentFK = models.ForeignKey(Channel, models.CASCADE, related_name="parent")

#TODO прописать, что обязательно есть канал у контента
class ContentRel(models.Model):
    contentFK = models.ForeignKey(Content, models.CASCADE)
    parentFK = models.ForeignKey(Channel, models.CASCADE)

