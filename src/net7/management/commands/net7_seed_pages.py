
from django.core.management.base import BaseCommand,CommandError
from pages.models import Pages

class Command(BaseCommand):
    help = 'Seed Pages'

    def handle(self, *args, **kwargs):

        Pages.objects.create(
            creator_id=1,
            name="Condizioni di utilizzo",
            slug="condizioni-di-utilizzo",
            content="<h1>Condizioni di utilizzo</h1>",
        )
        Pages.objects.create(
            creator_id=1,
            name="Criteri di moderazione & qualità",
            slug="criteri-di-moderazioni-qualita",
            content="<h1>Criteri di moderazione & qualità</h1>",
        )
        Pages.objects.create(
            creator_id=1,
            name="API",
            slug="api",
            content="<h1>API</h1>",
        )
        Pages.objects.create(
            creator_id=1,
            name="Privacy Policy",
            slug="privacy-policy",
            content="<h1>Privacy Policy</h1>",
        )
        Pages.objects.create(
            creator_id=1,
            name="Cookie Policy",
            slug="cookie-policy",
            content="<h1>Cookie Policy</h1>",
        )

        Pages.objects.create(
            creator_id=1,
            name="About",
            slug="about",
            content="<h1>About</h1>",
        )


