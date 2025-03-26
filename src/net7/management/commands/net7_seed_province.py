import csv
import os
from django.core.management.base import BaseCommand,CommandError
from projects.models import ProjectCountry
from organisations.models import Organisation
from organisations.models import OrganisationType
from django.conf import settings

class Command(BaseCommand):
    help = 'Seed projects'

    def handle(self, *args, **kwargs):

        project = ProjectCountry.objects.create(
            country='IT',
            country_name='Italy',  # row['Common'],
            longitude=42.638426,
            latitude=12.674724,
        )


        # basedir = os.path.dirname(settings.BASE_DIR)
        # csv_file = os.path.join(basedir, 'resources', 'Italy.csv')
        #
        # if not os.path.isfile(csv_file):
        #     raise CommandError(f"Il file {csv_file} non esiste.")
        #
        # self.stdout.write(f'Seeding database with data from {csv_file}')
        #
        # with open(csv_file, mode='r') as file:
        #     csv_reader = csv.DictReader(file)
        #     rows = list(csv_reader)
        #
        #     if not rows:
        #         raise ValueError("Il file CSV è vuoto o non contiene dati validi.")
        #
        #     for row in rows:
        #         status = self.getStatus(row['Common'])
        #         project = ProjectCountry.objects.create(
        #             country='IT',
        #             country_name='Italy', #row['Common'],
        #             longitude=42.638426,
        #             latitude=12.674724,
        #         )
        self.stdout.write('Database seeded successfully!')

    def getStatus(self,code):
        status = Status.objects.filter(status=code).first()
        if status == None:
            status = Status.objects.create(
                status=code,
                status_it=code,
            )
        return status

    def getOrganisations(self,data):
        org = Organisation.objects.filter(name=data['organisation']).first()
        if org == None:

            orgType = OrganisationType.objects.filter(type='default').first()
            if orgType == None:
                orgType = OrganisationType.objects.create(
                    type='default',
                    type_it='default',
                )
            org = Organisation.objects.create(
                name=data['organisation'],
                creator_id=1,
                orgType=orgType,
            )
        return org
