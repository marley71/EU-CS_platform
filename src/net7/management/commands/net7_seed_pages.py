
from django.core.management.base import BaseCommand,CommandError
from pages.models import Pages

class Command(BaseCommand):
    help = 'Seed Pages'

    def handle(self, *args, **kwargs):

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

        Pages.objects.create(
            creator_id=1,
            name="About",
            slug="about",
            content="About",
        )


