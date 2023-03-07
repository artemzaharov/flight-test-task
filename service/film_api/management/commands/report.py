from django.core.management.base import BaseCommand
from film_api.scoring import get_score_report

class Command(BaseCommand):
    help = 'Get report of channels score in csv file'

    def handle(self, *args, **options):
        print("Scoring...")
        file_content = get_score_report()
        print("done. Saving...")
        try:
            if len(args) > 0:
                filename = args[0]
            else:
                filename = "report.csv"
            with open(filename, "wt", encoding="utf-8") as f:
                f.write(file_content)
        except Exception:
            print("Cannot write to the specific file")
    
    def add_arguments(self, parser):
        parser.add_argument(
            nargs='+',
            type=str,
            dest = 'args'
        )