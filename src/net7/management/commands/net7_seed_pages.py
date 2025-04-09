
from django.core.management.base import BaseCommand,CommandError
from django.conf import settings
from pages.models import Pages
import os

class Command(BaseCommand):
    help = 'Seed Pages'

    def handle(self, *args, **kwargs):
        basedir = os.path.dirname(settings.BASE_DIR)
        Pages.objects.create(
            creator_id=1,
            name="Condizioni di utilizzo",
            slug="condizioni-di-utilizzo",
            content="Condizioni di utilizzo",
        )
        Pages.objects.create(
            creator_id=1,
            name="Criteri di moderazione & qualità",
            slug="criteri-di-moderazioni-qualita",
            content="Criteri di moderazione & qualità",
        )
        Pages.objects.create(
            creator_id=1,
            name="API",
            slug="api",
            content="API",
        )
        Pages.objects.create(
            creator_id=1,
            name="Privacy Policy",
            slug="privacy-policy",
            content="Privacy Policy",
        )
        Pages.objects.create(
            creator_id=1,
            name="Cookie Policy",
            slug="cookie-policy",
            content="Cookie Policy",
        )


        about_file = os.path.join(basedir, 'resources', 'about.htm')

        try:
            with open(about_file, 'r') as file:
                contenuto = file.read()
            Pages.objects.create(
                creator_id=1,
                name="About",
                slug="about",
                content=contenuto,
            )
        except FileNotFoundError:
            raise CommandError(f"Il file {about_file} non esiste.")
        except IOError:
            raise CommandError("Errore durante la lettura del file.")
