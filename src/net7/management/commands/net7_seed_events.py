import csv
import os
import random
from django.core.management.base import BaseCommand,CommandError
from events.models import Event
from organisations.models import Organisation
from organisations.models import OrganisationType
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seed projects'

    def handle(self, *args, **kwargs):

        basedir = os.path.dirname(settings.BASE_DIR)
        csv_file = os.path.join(basedir, 'resources', 'events - events.csv')

        if not os.path.isfile(csv_file):
            raise CommandError(f"Il file {csv_file} non esiste.")

        self.stdout.write(f'Seeding database with data from {csv_file}')

        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            rows = list(csv_reader)

            if not rows:
                raise ValueError("Il file CSV è vuoto o non contiene dati validi.")

            for row in rows:
                #status = self.getStatus(row['status'])
                organisation = self.getOrganisations(row)
                self.stdout.write(row['title'])

                # Data di partenza (oggi)
                data_inizio = datetime.now()

                # Genera un numero casuale di giorni da 1 a 30
                giorni_random = random.randint(1, 30)

                # Calcola la nuova data nel futuro
                data_futuro_start = data_inizio + timedelta(days=giorni_random)


                # Converti la stringa in un oggetto datetime
                date_object = datetime.strptime(row['start_date'], "%Y-%m-%d %H:%M:%S")
                # Assicurati che l'oggetto datetime sia consapevole del fuso orario
                start_date = timezone.make_aware(data_futuro_start)

                # Genera un numero casuale di giorni da 1 a 30
                giorni_random = random.randint(31, 60)

                data_futuro_end = data_inizio + timedelta(days=giorni_random)

                #date_object = datetime.strptime(row['end_date'], "%Y-%m-%d %H:%M:%S")
                end_date = timezone.make_aware(data_futuro_end)





                event = Event.objects.create(
                    title=row['title'],
                    description=row['description'],
                    description_it=row['description'],
                    url=row['url'],
                    latitude=random.uniform(40, 43),
                    longitude=random.uniform(6, 12),
                    #status_id=status.id,
                    approved=True,
                    start_date=start_date,
                    end_date=end_date,
                    event_type='online',
                    creator_id=1, # id superadmin
                    #organisation=organisation

                )
                event.organisations.add(organisation)
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
        return Organisation.objects.order_by('?').first()
        # org = Organisation.objects.filter(name=data['organisation']).first()
        # if org == None:
        #
        #     orgType = OrganisationType.objects.filter(type='default').first()
        #     if orgType == None:
        #         orgType = OrganisationType.objects.create(
        #             type='default',
        #             type_it='default',
        #         )
        #     org = Organisation.objects.create(
        #         name=data['organisation'],
        #         creator_id=1,
        #         orgType=orgType,
        #     )
        # return org
