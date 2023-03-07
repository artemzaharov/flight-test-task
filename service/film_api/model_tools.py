CONTENT_EMPTY_CONTENT_NAME = "Empty content"
CONTENT_EMPTY_CONTENT_TEXT = "Content to this channel has not been"


# Checks if the target channel is a descendant of the base channel
def find_channel_in_descendants(base_channel, target_channel):
    # if the current channel is the same as the one you are looking for, then you have found
    if base_channel.id == target_channel.id:
        return True
    else:
        # otherwise check that the desired channel is in the descendants of at least one of the subchannels
        return any([find_channel_in_descendants(channel, target_channel) for channel in base_channel.child_channels.get_queryset()])


