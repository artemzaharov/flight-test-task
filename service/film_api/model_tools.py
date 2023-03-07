CONTENT_EMPTY_CONTENT_NAME = "Empty content"
CONTENT_EMPTY_CONTENT_TEXT = "Content to this channel has not been"


# Проверяет, является ли целевой канал потомком базового
def find_channel_in_descendants(base_channel, target_channel):
    # если текущий канал совпадает с искомым, значит нашли
    if base_channel.id == target_channel.id:
        return True
    else:
        # иначе проверям, что искомый канал есть в потомках хотя бы одного из подканалов
        return any([find_channel_in_descendants(channel, target_channel) for channel in base_channel.child_channels.get_queryset()])


