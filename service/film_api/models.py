from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, pre_save, pre_delete, m2m_changed
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from film_api.model_tools import *
from django.conf.locale import LANG_INFO

class Channel(models.Model):
    name = models.CharField(max_length=200)
    language = models.CharField(max_length=10)
    image = models.ImageField()
    parents_count = models.IntegerField(default=0)
    content_count = models.IntegerField(default=0)
    subchannels_count = models.IntegerField(default=0)
    parentChannels = models.ManyToManyField("self", blank=True, default=None, symmetrical=False, related_name="child_channels")
    
    def __str__(self) -> str:
        lang = LANG_INFO[self.language]['name'] if self.language in LANG_INFO else self.language
        return f'{self.name}[{lang}]'

    def clean(self) -> None:
        # еще не сохранили self, значит не можем трогать self.parrentChannels
        if self.id == None:
            return
        if self.parentChannels.contains(self):
            raise ValidationError(_('Reversing rel is prohibited'))
        if any([find_channel_in_descendants(channel, self) for channel in self.child_channels.get_queryset()]):
            raise ValidationError(_('Cycling rel is prohibited'))


class Content(models.Model):
    score = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    metadata = models.JSONField(null=True, default=None, blank=True)
    parentChannels = models.ManyToManyField(Channel, default=None,related_name="child_contents")

    def __str__(self) -> str:
        return self.name


class ContentFile(models.Model):
    class FileType(models.TextChoices):
        VIDEO = "VI", _('Video file')
        PDF = "PF", _("PDF file")
        TEXT = "TX", _("Text file")

    file = models.FileField()
    fileType = models.CharField(
        choices=FileType.choices, default=FileType.VIDEO, max_length=2)
    contentFK = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="file")


def restrict_channel_instance(instance, removedContent=None, removedChannel=None):
    # сохраняем новый канал, либо удаляем все содержимое из канала:
    # добавляем в него пустое содержимое
    childContents = [el for el in instance.child_contents.all() if removedContent == None or removedContent.id != el.id]
    childChannels = [el for el in instance.child_channels.all() if removedChannel == None or removedChannel.id != el.id]

    if len(childChannels) == 0 and len(childContents) == 0:
        empty_content = Content.objects.get(name=CONTENT_EMPTY_CONTENT_NAME)
        empty_content.parentChannels.add(instance)
        empty_content.save()
        return
    # добавляем в ранее пустой канал содержимое: удаляем пустое содержимое
    if instance.child_contents.filter(name=CONTENT_EMPTY_CONTENT_NAME).exists():
        if  instance.child_contents.count() > 1 or instance.child_channels.count() > 0:
            empty_content = Content.objects.get(name=CONTENT_EMPTY_CONTENT_NAME)
            empty_content.parentChannels.remove(instance)
            empty_content.save()
        #else - случай, когда что-то меняем, но канал не был и не становится пустым
    

@receiver(post_save, sender=Channel)
def channel_pre_save(sender, instance, *args, **kwargs):
    instance.full_clean()
    
@receiver(post_save, sender=Channel)
def channel_post_save(sender, instance, *args, **kwargs):
    restrict_channel_instance(instance)

@receiver(m2m_changed, sender=Channel.parentChannels.through)
def channel_m2mchanged(sender, instance, action, *args, **kwargs):
    restrict_channel_instance(instance)
    instance.full_clean()
    for channel in instance.parentChannels.all():
        if action == 'pre_remove':
            restrict_channel_instance(channel, removedChannel=instance)
        else:
            restrict_channel_instance(channel)
        channel.subchannels_count  = channel.child_channels.count()
        channel.save()
    instance.parents_count = instance.parentChannels.count()
    instance.save()
    

@receiver(m2m_changed, sender=Content.parentChannels.through)
def content_m2mchanged(sender, instance, action, *args, **kwargs):
    # пустой контекст - ничего не делаем
    if instance.name == CONTENT_EMPTY_CONTENT_NAME:
        return
    # любой другой контекст - обновляем родительские каналы
    for channel in instance.parentChannels.all():
        if action == 'pre_remove':
            restrict_channel_instance(channel, removedContent=instance)
        else:
            restrict_channel_instance(channel)
        channel.content_count = channel.child_contents.count()
        channel.save()

@receiver(post_save, sender=Content)
def content_post_save(sender, instance, *args, **kwargs):
    #  пустой контекст - ничего не делаем
    if instance.name == CONTENT_EMPTY_CONTENT_NAME:
        return
    # любой другой контекст - обновляем родительские каналы
    [restrict_channel_instance(channel) for channel in instance.parentChannels.all()]

@receiver(pre_delete, sender=Content)
def content_post_delete(sender, instance, *args, **kwargs):
    [restrict_channel_instance(channel, removedContent=instance) for channel in instance.parentChannels.all()]

@receiver(pre_delete, sender=Channel)
def content_post_delete(sender, instance, *args, **kwargs):
    [restrict_channel_instance(channel, removedChannel=instance) for channel in instance.parentChannels.all()]
