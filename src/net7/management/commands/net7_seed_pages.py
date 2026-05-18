from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pages.models import Pages
import os

import shutil

class Command(BaseCommand):
    help = 'Seed Pages'

    def handle(self, *args, **kwargs):
        basedir = os.path.dirname(settings.BASE_DIR)


        condizioni_utilizzo_file = os.path.join(basedir, 'resources/pages', 'condizioni_utilizzo.htm')
        try:
            with open(condizioni_utilizzo_file, 'r') as file:
                contenuto = file.read()

            Pages.objects.create(
                creator_id=1,
                name="Politiche di utilizzo",
                name_it="Politiche di utilizzo",
                slug="condizioni-di-utilizzo",
                content=contenuto,
                content_it=contenuto,
            )
        except FileNotFoundError:
            raise CommandError(f"Il file {condizioni_utilizzo_file} non esiste.")
        except IOError:
            raise CommandError("Errore durante la lettura del file.")

        moderazione_file = os.path.join(basedir, 'resources/pages', 'moderazione.htm')
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


        privacy_file = os.path.join(basedir, 'resources/pages', 'privacy.htm')
        try:
            with open(privacy_file, 'r') as file:
                contenuto = file.read()
            Pages.objects.create(
                creator_id=1,
                name="Privacy & Cookie Policy",
                name_it="Privacy & Cookie Policy",
                slug="privacy-cookie-policy",
                content=contenuto,
                content_it=contenuto,
            )
        except FileNotFoundError:
            raise CommandError(f"Il file {privacy_file} non esiste.")
        except IOError:
            raise CommandError("Errore durante la lettura del file.")

        Pages.objects.create(
            creator_id=1,
            name="Contatti",
            name_it="Contatti",
            slug="contatti",
            content="Contatti",
            content_it="Contatti",
        )

        about_file = os.path.join(basedir, 'resources/pages', 'about.htm')
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

        external_file = os.path.join(basedir, 'resources/pages', 'risorse-esterne.htm')
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

        tutorialGeojson_file = os.path.join(basedir, 'resources/pages', 'tutorialGeojson.htm')
        try:
            with open(tutorialGeojson_file, 'r') as file:
                contenuto = file.read()
            Pages.objects.create(
                creator_id=1,
                name="Tutorial tool mappa",
                name_it="Tutorial tool mappa",
                slug="tutorial-geojson",
                content=contenuto,
                content_it=contenuto,
            )
        except FileNotFoundError:
            raise CommandError(f"Il file {tutorialGeojson_file} non esiste.")
        except IOError:
            raise CommandError("Errore durante la lettura del file.")