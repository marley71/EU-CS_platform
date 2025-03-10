import csv
from django.core.management.base import BaseCommand
from projects.models import Project,Status

class Command(BaseCommand):
    help = 'Seed the database with initial data'
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file projects')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        self.stdout.write(f'Seeding database with data from {csv_file}')

        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                status = self.getStatus(row['status'])
                self.stdout.write(row['name'])
                Project.objects.create(
                    name=row['name'],
                    url=row['url'],
                    status_id=status.id,
                    creator_id=1, # id superadmin
                )
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
