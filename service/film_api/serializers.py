from rest_framework import serializers
from film_api import models as m
from django.db import IntegrityError
from film_api.tools import *


# # рекурсивное поле, глубины 1. Позволяет сослаться в сериализаторе на самого себя, но без дальнейшей рекурсии
# class RecursiveField(serializers.Serializer):
#     def to_representation(self, value):
#         serializer = self.parent.parent.__class__(value, context=self.context)
#         return serializer.data

class ContentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.ContentFile
        fields = ['id', 'file', 'fileType']

class ContentSerializer(serializers.ModelSerializer):
    file = ContentFileSerializer(required=False)

    class Meta:
        model = m.Content
        fields = ['id', 'name', 'metadata', 'score', 'file']

class OneChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model  = m.Channel
        fields = ['id', 'name']


class ChannelInTreeSerialier(serializers.ModelSerializer):
    childs = serializers.SerializerMethodField("get_childs")
 
    class Meta:
        model = m.Channel
        fields = ['id', 'name', 'childs']

    # def get_childs(self, instance):
    #     stack = channel_to_subchannels(instance)
    #     childs = []
    #     for subchannel in stack:
    #         dct = OneChannelSerializer(subchannel).data
    #         subchannel.dct_representation = dct
    #         childs.append(dct)
        
    #     while len(stack) > 0:
    #         current = stack.pop()
    #         content_childs = channel_to_content_childs(current)
    #         subchannel_childs = channel_to_subchannels(current)
    #         if len(content_childs) != 0 and len(subchannel_childs) != 0:
    #             raise IntegrityError("Db in faulted state: content and subchannels in the same channel")
    #         current.dct_representation['childs'] = []
    #         for content in content_childs:
    #             current.dct_representation['childs'].append(ContentSerializer(content).data)
    #         for subchannel in subchannel_childs:
    #             dct = OneChannelSerializer(subchannel).data
    #             subchannel.dct_representation = dct
    #             current.dct_representation['childs'].append(dct)
    #             stack.append(subchannel)

    #     childs.extend(channel_to_content_childs(instance))        
    #     return childs


    def get_childs(self, instance):
        content_childs = channel_to_content_childs(instance)
        if len(content_childs)>  0:
            return [ContentSerializer(content).data for content in content_childs]
        subchannels = channel_to_subchannels(instance)
        return [ChannelInTreeSerialier(channel).data for channel in subchannels]

class ForestSerializer(serializers.Serializer):
    channels = ChannelInTreeSerialier( many=True, read_only = True)