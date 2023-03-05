from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from film_api.serializers import *
from film_api.models import *
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

# Create your views here.
class ChannelView(GenericAPIView):
    permission_classes = (permissions.AllowAny,) 

    def get(self, requst, *args, **kwargs):
        if 'id' in kwargs:
            id = kwargs['id']
            channels = Channel.objects.filter(id=id)
            if len(channels) == 0:
                return Response(status=404, data=f"Channl with id {id} not exists")
            channel = channels[0]
            return Response(data=ChannelInTreeSerialier(channel).data, status=200)
        else:
            forest = get_channel_forest()
            return Response(status=200, data=ForestSerializer(forest).data)
    

class ContentViewSet(ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = (permissions.AllowAny,)

