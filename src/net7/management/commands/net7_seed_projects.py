import csv
import os
import random
from decimal import Decimal
from django.core.management.base import BaseCommand,CommandError
from projects.models import Project,Status,Keyword,Topic,HasTag, GeographicExtend, Provincia
from organisations.models import Organisation
from localita.models import Localita
#from provincia.models import Provincia
from organisations.models import OrganisationType
from django.conf import settings
from django.core.files import File
from django.db.models import Q
#from datetime import datetime, timedelta
from django.utils import timezone
from authtools.models import User
from profiles.models import Profile
import datetime

class Command(BaseCommand):
    help = 'Seed projects'

    def add_arguments(self, parser):
        # Argomento opzionale "type" con valore predefinito "bio"
        parser.add_argument(
            '--type',
            type=str,  # Specifica il tipo di dato
            default='all',  # Valore predefinito
            help='default tutti, bio solo biodiversity e normal gli altri'  # Descrizione dell'argomento
        )

    def handle(self, *args, **kwargs):
        type_value = kwargs['type']  # Ottieni il valore dell'argomento

        self.stdout.write(self.style.SUCCESS(f'Valore di type: {type_value}'))
        if type_value == 'all':
            self.normalProjects()
            self.weeklyProjects()
        elif type_value == 'bio':
            self.weeklyProjects()
        elif type_value == 'normal':
            self.normalProjects()
        else:
            self.stdout.write(self.style.ERROR(f'Valore di type: {type_value} non valido'))
        self.stdout.write('Database seeded successfully!')

    def normalProjects(self):
        basedir = os.path.dirname(settings.BASE_DIR)
        #csv_file = os.path.join(basedir, 'resources', 'Progetti di CS esistenti in seno a NBFC (Risposte)_TL.csv')
        csv_file = os.path.join(basedir, 'resources', 'progetti_agosto2025 (2).csv')
        if not os.path.isfile(csv_file):
            raise CommandError(f"Il file {csv_file} non esiste.")

        self.stdout.write(f'Seeding database with data from {csv_file}')

        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            rows = list(csv_reader)

            if not rows:
                raise ValueError("Il file CSV è vuoto o non contiene dati validi.")

            start_period = "2020-04-01 00:00:00"
            end_period = "2025-07-31 23:59:59"

            for row in rows:
                if not 'PROVINCE' in row:
                    raise ValueError("Il file CSV non contiene la colonna PROVINCE.")


                status = self.getStatus(row['Stato di attività'])

                # country = ProjectCountry.objects.filter(country_name=row['Regione']).first()
                #localita = Localita.objects.filter(name=row['Regione']).first()
                # keyword = Keyword.objects.filter(keyword='Importazione').first()
                self.stdout.write(row['Nome del progetto'])
                #start_date, end_date = self.generate_start_end_dates(start_period, end_period)

                if not row['Data Inizio']:
                    row['Data Inizio'] = "01/01/2025"
                start_date = datetime.datetime.strptime(row['Data Inizio'], "%d/%m/%Y")
                end_date = None
                if row['Data Fine']:
                    end_date = datetime.datetime.strptime(row['Data Fine'], "%d/%m/%Y")

                latitude = 41.53
                longitude = 12.28
                if row['Lat'] and row['Lng']:
                    latitude = row['Lat']
                    longitude = row['Lng']
                organisation = self.getOrganisations(row,latitude,longitude)
                user_id = self.getUser(row)
                self.stdout.write(' utente ' + str(user_id))
                project = Project.objects.create(
                    type=row['Tipo'],
                    name=row['Nome del progetto'],
                    citizen_science_aspects_description=row['Descrizione degli aspetti di CS (ad esempio in base ai 10 principi di ECSA).'],
                    # description=row['Descrizione degli aspetti di CS (ad esempio in base ai 10 principi di ECSA).'],
                    # description_it=row['Descrizione degli aspetti di CS (ad esempio in base ai 10 principi di ECSA).'],
                    aim=row['Scopo principale del progetto'],
                    aim_it=row['Scopo principale del progetto'],
                    url=row['Sito web di riferimento'],
                    status_id=status.id,
                    approved=True,
                    creator_id=user_id,  # id superadmin
                    mainOrganisation=organisation,
                    # country=country.country,
                    start_date=timezone.make_aware(start_date),
                    end_date=timezone.make_aware(end_date) if end_date else None,
                    dateUpdated=timezone.make_aware(end_date) if end_date else timezone.make_aware(datetime.datetime.now()),
                    #localita_id=localita.id,
                    localita_id = 1,
                    projectlocality=row['Luogo di svolgimento del progetto (città, provincia)'],
                    longitude=longitude,
                    latitude=latitude,
                    # keyword=keyword.keyword,
                    # organisation=organisation
                )


                # project.projectCountry.add(country)
                project.organisation.add(organisation)

                # project.keywords.add(keyword)
                self.setKeywords(project, row)
                self.setImage(project, row)
                self.setGeograficExtend(project, row)
                self.setProvince(project, row)

                provincia = project.provincia.first()
                if provincia:
                    project.latitude = provincia.latitude
                    project.longitude = provincia.longitude
                    project.save()
                    organisation.latitude = provincia.latitude
                    organisation.longitude = provincia.longitude
                    organisation.save()



    def weeklyProjects(self):
        basedir = os.path.dirname(settings.BASE_DIR)
        csv_file = os.path.join(basedir, 'resources', 'File progetto biodiversity sampling week_FINALE_05052025.csv')

        if not os.path.isfile(csv_file):
            raise CommandError(f"Il file {csv_file} non esiste.")

        self.stdout.write(f'Seeding database with data from {csv_file}')

        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            rows = list(csv_reader)

            if not rows:
                raise ValueError("Il file CSV è vuoto o non contiene dati validi.")

            start_period = "2020-01-01 00:00:00"
            end_period = "2025-07-31 23:59:59"

            for row in rows:
                status = self.getStatus(row['Stato di attività'])
                organisation = self.getOrganisations(row)
                # country = ProjectCountry.objects.filter(country_name=row['Regione']).first()
                self.stdout.write(f'cerco provincia (' + str(row['PROVINCIA']) + ')')

                provincia = Provincia.objects.filter(sigla=str(row['PROVINCIA']).strip()).first()
                localita = Localita.objects.filter(name=provincia.regione).first()
                # keyword = Keyword.objects.filter(keyword='Importazione').first()
                self.stdout.write(row['Nome del progetto'])
                start_date, end_date = self.generate_start_end_dates(start_period, end_period)
                start_date = datetime.strptime(row['Data Inizio'], "%d/%m/%Y")
                end_date = datetime.strptime(row['Data Fine'], "%d/%m/%Y")
                email = str(row['email']).strip()
                project = Project.objects.create(
                    name=row['Nome del progetto'],
                    description=row['Descrizione'],
                    description_it=row['Descrizione'],
                    aim=' ', #row['Scopo principale del progetto'],
                    aim_it=' ', #row['Scopo principale del progetto'],
                    url=row['Sito web di riferimento'],
                    status_id=status.id,
                    approved=True,
                    creator_id=1,  # id superadmin
                    mainOrganisation=organisation,
                    # country=country.country,
                    start_date=timezone.make_aware(start_date),
                    end_date=timezone.make_aware(end_date),
                    dateUpdated=timezone.make_aware(end_date),
                    localita_id=localita.id,
                    #provincia_id=provincia.id,
                    author=row['Contatti'],
                    author_email=email,
                    projectlocality=row['Luogo di svolgimento del progetto (città, provincia)'],
                    # keyword=keyword.keyword,
                    # organisation=organisation
                )
                # project.projectCountry.add(country)
                project.organisation.add(organisation)
                if provincia:
                    project.provincia.add(provincia)
                    project.latitude = provincia.latitude
                    project.longitude = provincia.longitude
                elif localita:
                    project.latitude = localita.latitude
                    project.longitude = localita.longitude

                # project.keywords.add(keyword)
                row['TAGs/Keywords'] = "biodiversity sampling week" #forzo la keyword a questa
                self.setKeywords(project, row)
                self.setImageBsw(project, row)
                self.setGeograficExtend(project, row)

    def getStatus(self,code):
        status = Status.objects.filter(status_code=code).first()
        if status == None:
            raise ValueError('Stato progetto non valido ' + code)
#             status = Status.objects.create(
#                 status=code,
#                 status_it=code,
#             )
        return status

    def getOrganisations(self,row,latitude,longitude):
        org = Organisation.objects.filter(name=row['Principale organizzazione promotrice']).first()
        if org == None:
            #localita = Localita.objects.filter(name=row['Regione']).first()
            #self.stdout.write('localita ' + localita.name + ' ' + str(localita.id))
            orgType = OrganisationType.objects.filter(type='default').first()
            if orgType == None:
                orgType = OrganisationType.objects.create(
                    type='default',
                    type_it='default',
                )
            #latitudine, longitudine = self.genera_coordinate_italia()
            #quantita_casuale = Decimal(str(random.uniform(0.05, 0.20)))
            #latitudine = localita.latitude + quantita_casuale
            #quantita_casuale = Decimal(str(random.uniform(0.05, 0.20)))
            #longitudine = localita.longitude + quantita_casuale

            org = Organisation.objects.create(
                name=row['Principale organizzazione promotrice'],
                creator_id=1,
                orgType=orgType,
                latitude=latitude,
                longitude=longitude,
                localita_id=1 #localita.id,
            )
        return org

    def getUser(self,row):
        if not row['Email utente']:
            return 1
        user = User.objects.filter(email=row['Email utente']).first()
        if user == None:
            user = User.objects.create(
                password=row['Email utente'].split('@')[0],
                is_superuser=False,
                email=row['Email utente'],
                is_staff=False,
                is_active=True,
                name=row['Email utente'].split('@')[0],
            )
            profile = Profile.objects.get(pk=user.id)
            profile.surname = user.name
            profile.profileVisible = True
            profile.save()

        return user.id

    def genera_coordinate_italia(self):
        latitudine = random.uniform(36.6, 47.1)
        longitudine = random.uniform(6.6, 18.5)
        return latitudine, longitudine

    def setImageBsw(self,project,row):
        image_path = str(settings.BASE_DIR) + '/../resources/demo/foto_BSW/' + row['immagine']
        self.stdout.write('base path ' + image_path)
        # Associa il file immagine al modello
        with open(image_path, 'rb') as image_file:
            project.image1.save(row['immagine'], File(image_file), save=True)

    def setImage(self,project,row):
        image_path = str(settings.BASE_DIR) + '/../resources/demo/Immagini_progetti/' + row['immagine']
        self.stdout.write('base path ' + image_path)
        # Associa il file immagine al modello
        with open(image_path, 'rb') as image_file:
            project.image1.save(row['immagine'], File(image_file), save=True)

        # numero_casuale = random.randint(1, 10)
        # image_path = str(settings.BASE_DIR) + '/../resources/demo/images/p' + str(numero_casuale) + '.png'
        # self.stdout.write('base path ' + image_path )
        # # Associa il file immagine al modello
        # with open(image_path, 'rb') as image_file:
        #     project.image1.save(str(project.id) + str(numero_casuale) + '.png', File(image_file), save=True)

    def setGeograficExtend(self,project,row):
        if not row['Entità geografica del progetto']:
            return
        text = str(row['Entità geografica del progetto'])
        ge = GeographicExtend.objects.get_or_create(geographicextend=text.strip())
        project.geographicextend.add(ge[0])


    def setKeywords(self,project,row):
        if not row['Keywords']:
            return
        keywords = str(row['Keywords'])
        for keyword in keywords.split(','):
            kModel = Keyword.objects.get_or_create(keyword=keyword.strip())
            self.stdout.write(kModel[0].keyword)
            project.keywords.add(kModel[0])

        # descriptions = list(Keyword.objects.exclude(
        #     Q(keyword="Importazione") ).values_list('keyword',flat=True))
        # for i in range(1, 5):
        #     random_description = random.choice(descriptions)  # Prendi un elemento casuale
        #     descriptions.remove(random_description)  # Rimuovilo dalla lista
        #     keyword = Keyword.objects.filter(keyword=random_description).first()
        #     project.keywords.add(keyword)
        #
        # topics = list(Topic.objects.all().values_list('topic', flat=True))
        # for i in range(1, 4):
        #     random_description = random.choice(topics)  # Prendi un elemento casuale
        #     topics.remove(random_description)  # Rimuovilo dalla lista
        #     topic = Topic.objects.filter(topic=random_description).first()
        #     project.topic.add(topic)
        #
        # hastags = list(HasTag.objects.all().values_list('hasTag', flat=True))
        # for i in range(1, 4):
        #     random_description = random.choice(hastags)  # Prendi un elemento casuale
        #     hastags.remove(random_description)  # Rimuovilo dalla lista
        #     hastag = HasTag.objects.filter(hasTag=random_description).first()
        #     project.hasTag.add(hastag)

    def generate_start_end_dates(self,startDate, endDate):
        # Converti le date in oggetti datetime
        start_date = datetime.strptime(startDate, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(endDate, "%Y-%m-%d %H:%M:%S")

        # Calcola la differenza tra le due date
        delta = end_date - start_date

        # Genera un numero casuale di giorni per start_date
        random_start_days = random.randint(0, delta.days)

        # Crea start_date
        generated_start_date = start_date + timedelta(days=random_start_days)

        # Calcola il numero di giorni rimanenti per end_date
        remaining_days = delta.days - random_start_days

        # Genera un numero casuale di giorni per end_date, garantendo che sia dopo start_date
        if remaining_days > 0:
            random_end_days = random.randint(1, remaining_days)
            generated_end_date = generated_start_date + timedelta(days=random_end_days)
        else:
            # Se non ci sono giorni rimanenti, end_date deve essere uguale a start_date, ma spostata in avanti (1 giorno)
            generated_end_date = generated_start_date + timedelta(days=1)

        return generated_start_date, generated_end_date

    def setProvince(self,project,row):
        province = row['PROVINCE'].split(';')
        if (not province):
            self.stdout.write(f'il progetto ' + str(project.id) + ' non ha province ')
            return
        for provincia in province:
            if len(provincia.strip()) == 2:
                #la considero una sigla.
                provObj = Provincia.objects.filter(sigla__iexact=provincia.strip()).first()
            else:
                provObj = Provincia.objects.filter(nome__iexact=provincia.strip()).first()

            if provObj == None:
                self.stdout.write(f'il progetto ' + str(project.id) + ' provincia non trovata con  ' + provincia.strip())
            else:
                project.provincia.add(provObj)


