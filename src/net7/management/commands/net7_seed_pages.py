from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pages.models import Pages
import os

import shutil

class Command(BaseCommand):
    help = 'Seed Pages'

    def handle(self, *args, **kwargs):
        basedir = os.path.dirname(settings.BASE_DIR)
        Pages.objects.create(
            creator_id=1,
            name="Condizioni di utilizzo",
            name_it="Condizioni di utilizzo",
            slug="condizioni-di-utilizzo",
            content="Condizioni di utilizzo",
            content_it="Condizioni di utilizzo",
        )

        moderazione_file = os.path.join(basedir, 'resources', 'moderazione.htm')

        try:
            with open(moderazione_file, 'r') as file:
                contenuto = file.read()
            Pages.objects.create(
                creator_id=1,
                name="Criteri di moderazione & qualità",
                name_it="Criteri di moderazione & qualità",
                slug="criteri-di-moderazioni-qualita",
                content=contenuto,
                content_it=contenuto,
            )
        except FileNotFoundError:
            raise CommandError(f"Il file {moderazione_file} non esiste.")
        except IOError:
            raise CommandError("Errore durante la lettura del file.")

        Pages.objects.create(
            creator_id=1,
            name="API",
            name_it="API",
            slug="api",
            content="API",
            content_it="API",
        )
        Pages.objects.create(
            creator_id=1,
            name="Privacy Policy",
            name_it="Privacy Policy",
            slug="privacy-policy",
            content="Privacy Policy",
            content_it="Privacy Policy",
        )
        Pages.objects.create(
            creator_id=1,
            name="Cookie Policy",
            name_it="Cookie Policy",
            slug="cookie-policy",
            content="Cookie Policy",
            content_it="Cookie Policy",
        )

        about_file = os.path.join(basedir, 'resources', 'about.htm')

        try:
            with open(about_file, 'r') as file:
                contenuto = file.read()
            Pages.objects.create(
                creator_id=1,
                name="About",
                name_it="About",
                slug="about",
                content=contenuto,
                content_it=contenuto,
            )
        except FileNotFoundError:
            raise CommandError(f"Il file {about_file} non esiste.")
        except IOError:
            raise CommandError("Errore durante la lettura del file.")

        external_file = os.path.join(basedir, 'resources', 'risorse-esterne.htm')

        try:
            with open(external_file, 'r') as file:
                contenuto = file.read()
                Pages.objects.create(
                    creator_id=1,
                    name="External Resources",
                    name_it="Risorse esterne",
                    slug="external-resources",
                    content=contenuto,
                    content_it=contenuto,
                )
        except FileNotFoundError:
            raise CommandError(f"Il file {external_file} non esiste.")
        except IOError:
            raise CommandError("Errore durante la lettura del file.")

        shutil.copy(basedir + "/resources/images/pages/biodiversitygateway.png",basedir + "/src/media/images/biodiversitygateway.png")
        shutil.copy(basedir + "/resources/images/pages/eu-citizen-science.svg",basedir + "/src/media/images/eu-citizen-science.svg")
        shutil.copy(basedir + "/resources/images/pages/logo-csi_1-800x255.png",basedir + "/src/media/images/logo-csi_1-800x255.png")
        shutil.copy(basedir + "/resources/images/pages/Logo_NBFC.png",basedir + "/src/media/images/Logo_NBFC.png")
