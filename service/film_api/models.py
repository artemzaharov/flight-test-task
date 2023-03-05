from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


class Content(models.Model):
    score = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    metadata = models.JSONField(null=True, default=None)
    parents_count = models.IntegerField(default=0)


class ContentFile(models.Model):
    class FieldType(models.TextChoices):
        VIDEO = "VI", _('Video file')
        PDF = "PF", _("PDF file")
        TEXT = "TX", _("Text file")

    file = models.FileField()
    fileType = models.CharField(
        choices=FieldType.choices, default=FieldType.VIDEO, max_length=2)
    contentFK = models.ForeignKey(Content, on_delete=models.CASCADE)


class Channel(models.Model):
    name = models.CharField(max_length=200)
    parents_count = models.IntegerField(default=0)


class ParentChannelRel(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["channelFK", "parentFK"], name="unique_channel_rel"
            ),
        ]

    channelFK = models.ForeignKey(Channel, models.CASCADE, related_name="channel_parents")
    parentFK = models.ForeignKey(
        Channel, models.CASCADE, related_name="channel_subchannels")
    

    def clean(self) -> None:
        if self.channelFK.id == self.parentFK.id:
            raise ValidationError(_('Reversing rel is prohibited'))
        if ParentChannelRel.objects.filter(channelFK=self.parentFK, parentFK=self.channelFK).count() > 0:
            raise ValidationError(_('Cycling rel is prohibited'))

class ContentRel(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["contentFK", "parentFK"], name="unique_content_rel"
            ),

        ]
    contentFK = models.ForeignKey(
        Content, models.CASCADE, related_name="content_channels")
    parentFK = models.ForeignKey(Channel, models.CASCADE, related_name="channel_contents")


@receiver(post_save, sender=ContentRel)
def content_rel_post_save(sender, instance, *args, **kwargs):
    content = instance.contentFK
    content.parents_count = ContentRel.objects.filter(contentFK=content).count()
    content.save()

@receiver(post_save, sender=ParentChannelRel)
def content_rel_post_save(sender, instance, *args, **kwargs):
    channel = instance.channelFK
    channel.parents_count = ParentChannelRel.objects.filter(channelFK=channel).count()
    channel.save()


@receiver(pre_save)
def all_pre_save(sender, instance, *args, **kwargs):
    instance.full_clean()