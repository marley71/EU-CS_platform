import csv
import os
import random
from django.core.management.base import BaseCommand,CommandError
from projects.models import Project,Status,ProjectCountry,Keyword
from organisations.models import Organisation
from organisations.models import OrganisationType
from django.conf import settings
from django.core.files import File
from django.db.models import Q

class Command(BaseCommand):
    help = 'Seed projects'

    def handle(self, *args, **kwargs):

        basedir = os.path.dirname(settings.BASE_DIR)
        csv_file = os.path.join(basedir, 'resources', 'Progetti_di_CS.csv')

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
                country = ProjectCountry.objects.filter(country='IT').first()
                keyword = Keyword.objects.filter(keyword='Importazione').first()
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
                    mainOrganisation=organisation,
                    country=country.country,
                    #keyword=keyword.keyword,
                    #organisation=organisation
                )
                project.organisation.add(organisation)
                project.keywords.add(keyword)
                self.setKeywords(project)
                self.setImage(project)
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
            latitudine, longitudine = self.genera_coordinate_italia()
            org = Organisation.objects.create(
                name=data['organisation'],
                creator_id=1,
                orgType=orgType,
                latitude=latitudine,
                longitude=longitudine,

            )
        return org

    def genera_coordinate_italia(self):
        latitudine = random.uniform(36.6, 47.1)
        longitudine = random.uniform(6.6, 18.5)
        return latitudine, longitudine

    def setImage(self,project):
        numero_casuale = random.randint(1, 10)
        image_path = str(settings.BASE_DIR) + '/../resources/demo/images/p' + str(numero_casuale) + '.png'
        self.stdout.write('base path ' + image_path )
        # Associa il file immagine al modello
        with open(image_path, 'rb') as image_file:
            project.image1.save(str(project.id) + str(numero_casuale) + '.png', File(image_file), save=True)

    def setKeywords(self,project):
        descriptions = list(Keyword.objects.exclude(
            Q(keyword="Importazione") ).values_list('keyword',flat=True))
        for i in range(1, 5):
            random_description = random.choice(descriptions)  # Prendi un elemento casuale
            descriptions.remove(random_description)  # Rimuovilo dalla lista
            keyword = Keyword.objects.filter(keyword=random_description).first()
            project.keywords.add(keyword)