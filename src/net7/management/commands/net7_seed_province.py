import json
import os
from django.core.management.base import BaseCommand,CommandError

from profiles.views import projects

#from provincia.models import Provincia
from projects.models  import Provincia
from django.conf import settings

class Command(BaseCommand):
    help = 'Seed projects'

    def handle(self, *args, **kwargs):

        # project = ProjectCountry.objects.create(
        #     country='IT',
        #     country_name='Italy',  # row['Common'],
        #     longitude=42.638426,
        #     latitude=12.674724,
        # )


        basedir = os.path.dirname(settings.BASE_DIR)
        file_path = os.path.join(basedir, 'resources', 'province.json')

        if not os.path.isfile(file_path):
            raise CommandError(f"Il file {file_path} non esiste.")

        self.stdout.write(f'Seeding database with data from {file_path}')

        with open(file_path, mode='r') as file:
            data = json.load(file)

        for provincia in data:
            Provincia.objects.create(
                nome=provincia['provincia'],
                sigla=provincia['sigla'],
                regione=provincia['regione'],
                latitude=provincia['coordinate']['latitude'],
                longitude=provincia['coordinate']['longitude'],
            )

        self.stdout.write('Database seeded successfully!')
