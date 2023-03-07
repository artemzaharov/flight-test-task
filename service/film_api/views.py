from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from film_api.serializers import *
from film_api.models import *
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.http import FileResponse

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

class ContentFileDownload(GenericAPIView):
    permission_classes = (permissions.AllowAny,) 
    
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            pk = kwargs['pk']
            contentFile = ContentFile.objects.filter(id=pk)
            if len(contentFile) == 0:
                return Response(status=404)
            contentFile = contentFile[0]
            resp =  FileResponse(contentFile.file.file)
            if contentFile.fileType ==  ContentFile.FileType.TEXT:
                resp['Content-Type'] = 'text/plain'
            elif contentFile.fileType ==  ContentFile.FileType.PDF:
                resp['Content-Type'] = 'application/pdf'
            else:
                resp['Content-Type'] = 'video/x-ms-wmv'
            return resp
        return Response(status=400, data="No pk given")
