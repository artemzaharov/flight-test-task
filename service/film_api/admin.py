from django.contrib import admin
from film_api.models import *
from film_api.tools import *


class ContentAdmin(admin.ModelAdmin):
    exclude = ('parents_count',)
    filter_horizontal = ('parentChannels',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "parentChannels":
            # возвращаем только те каналы, которые не содержат подканалов
            kwargs["queryset"] = Channel.objects.filter(subchannels_count=0)
        return super(ContentAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

class ChannelAdmin(admin.ModelAdmin):
    exclude = ('parents_count', 'content_count', 'subchannels_count')
    filter_horizontal = ('parentChannels',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "parentChannels":
            # получаем все каналы, которые могут быть родительскими, т.е. которые не содержат контент
            channelsWithoutContent = Channel.objects.filter(content_count=0) 
            if 'object_id' in request.resolver_match.kwargs:
                # получаем  канал, для которого запрашиваем список
                pk = request.resolver_match.kwargs['object_id']
                channel = Channel.objects.get(pk=pk)
                # получаем список всех потомков (тут рекурсия вплоть до листьев)
                all_descendants = recursive_query_all_descendans_channels(channel)
                # выбираем id потомков
                all_descendants = [el.id for el in all_descendants]
                channelsWithoutContent =  channelsWithoutContent.exclude(pk__in=all_descendants)
            # возрващаем все потенциальные родительские каналы, не являющиеся потомком текущего
            kwargs["queryset"] = channelsWithoutContent
        return super(ChannelAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
    
admin.site.register(Content, ContentAdmin)
admin.site.register(Channel, ChannelAdmin)