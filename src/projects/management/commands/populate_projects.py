import csv
import os
from django.core.management.base import BaseCommand,CommandError
from projects.models import Project,Status
from organisations.models import Organisation

from organisations.models import OrganisationType


class Command(BaseCommand):
    help = 'Seed the database with initial data'
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file projects')

    def handle(self, *args, **kwargs):
        if len(kwargs) == 0:
            raise CommandError(f"Il file csv non passato.")

        csv_file = kwargs['csv_file']

        if not os.path.isfile(csv_file):
            raise CommandError(f"Il file {csv_file} non esiste.")

        self.stdout.write(f'Seeding database with data from {csv_file}')

        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            rows = list(csv_reader)

            if not rows:
                raise ValueError("Il file CSV è vuoto o non contiene dati validi.")

            for row in rows:
                status = self.getStatus(row['status'])
                organisation = self.getOrganisations(row)
                self.stdout.write(row['name'])
                project = Project.objects.create(
                    name=row['name'],
                    description=row['description'],
                    description_it=row['description'],
                    aim=row['aim'],
                    aim_it=row['aim'],
                    url=row['url'],
                    status_id=status.id,
                    approved=True,
                    creator_id=1, # id superadmin
                    #organisation=organisation
                )
                project.organisation.add(organisation)
#                 MyModel.objects.create(
#                     name=row['name'],
#                     description=row['description']
#                 )

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
