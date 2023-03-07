from django.apps import AppConfig
from django.db.utils import ProgrammingError

class FilmApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'film_api'

    def ready(self) -> None:
        try:
            from film_api.models  import Channel, Content
            from film_api.tools import CONTENT_EMPTY_CONTENT_NAME, CONTENT_EMPTY_CONTENT_TEXT

            if not Content.objects.filter(name=CONTENT_EMPTY_CONTENT_NAME).exists():
                content = Content(name=CONTENT_EMPTY_CONTENT_NAME)
                content.metadata={'text':CONTENT_EMPTY_CONTENT_TEXT}
                content.save()
        except ProgrammingError:
            # we are in migration
            pass