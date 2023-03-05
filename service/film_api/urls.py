from django.urls import path
from film_api.views import *


urlpatterns = [
    path('api/channel', ChannelView.as_view()),
    path('api/channel/<int:id>', ChannelView.as_view()),
    path('api/content/<int:pk>', ContentViewSet.as_view({
        'get': 'retrieve',
        })
    ),

]
