from rest_framework import serializers
from film_api import models as m

class ContentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.ContentFile
        fields = ['id', 'file', 'fileType']

class ContentSerializer(serializers.ModelSerializer):
    file = ContentFileSerializer(required=False)

    class Meta:
        model = m.Content
        fields = ['id', 'name', 'metadata', 'score', 'file']

class ChannelSerializer(serializers.ModelSerializer):
    content_childs = ContentSerializer(many=True, read_only = True, required=False)
    class Meta:
        model = m.Channel
        fields = ['id', 'name', 'content_childs' ]

class ChannelInTreeSerialier(ChannelSerializer):
    channel_childs = ChannelSerializer(many=True, read_only = True, required=False)
    
    class Meta:
        model = m.Channel
        fields = ['id', 'name', 'content_childs', 'channel_childs']


    def validate(self, data):
        if not ('channel_childs' in data or 'content_childs' in data):
            raise serializers.ValidationError("'content_childs' or 'channel_childs' must be presented")        
        validated_data = super().validate(data)
        if 'channel_childs' in data:
            validated_data['channel_childs'] = data['channel_childs']
        if 'content_childs' in data:
            validated_data['content_childs'] = data['content_childs']


class TreeSerializer(serializers.Serializer):
    channel_childs = ChannelInTreeSerialier(many=True, read_only = True)