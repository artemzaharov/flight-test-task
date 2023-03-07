from rest_framework import serializers
from film_api import models as m
from django.db import IntegrityError
from film_api.tools import *
from service.settings import MEDIA_ROOT
import os.path as p

class ContentFileSerializer(serializers.ModelSerializer):
    path = serializers.SerializerMethodField("get_file_path")
    class Meta:
        model = m.ContentFile
        fields = ['id', 'path', 'fileType']

    def get_file_path(self, instance):
        file_path = p.basename(instance.file.path)
        return file_path

class ContentSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField("get_file")
    
    class Meta:
        model = m.Content
        fields = ['id', 'name', 'metadata', 'score', 'file']
    
    def get_file(self, instance):
        if instance.file.values().count() > 0:
            return ContentFileSerializer(instance=instance.file.get_queryset()[0]).data
        return None


class OneChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model  = m.Channel
        fields = ['id', 'name', 'language', 'image']


class ChannelInTreeSerialier(serializers.ModelSerializer):
    childs = serializers.SerializerMethodField("get_childs")
 
    class Meta:
        model = m.Channel
        fields = ['id', 'name','language', 'image',  'childs']

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