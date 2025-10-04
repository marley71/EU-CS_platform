import csv
import os
from django.core.management.base import BaseCommand,CommandError
from authtools.models import User
from profiles.models import Profile
from django.conf import settings

class Command(BaseCommand):
    help = 'Seed users'

    def handle(self, *args, **kwargs):
        basedir = os.path.dirname(settings.BASE_DIR)
        # csv_file = os.path.join(basedir, 'resources', 'Progetti di CS esistenti in seno a NBFC (Risposte)_TL.csv')
        csv_file = os.path.join(basedir, 'resources', 'utenti_moderatori.csv')
        if not os.path.isfile(csv_file):
            raise CommandError(f"Il file {csv_file} non esiste.")

        self.stdout.write(f'Seeding database with data from {csv_file}')

        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            rows = list(csv_reader)

            if not rows:
                raise ValueError("Il file CSV è vuoto o non contiene dati validi.")

            for row in rows:
                if row['Email']:
                    user = self.createUser(row)
                    self.updateProfile(user)

        self.stdout.write('Database seeded successfully!')

    def createUser(self,row):
        user = User.objects.filter(email=row['Email']).first()
        if user == None:
            user = User.objects.create(
                password=row['Email'].split('@')[0],
                is_superuser=False,
                email=row['Email'],
                is_staff=True,
                is_active=True,
                name=row['Nome e Cognome'],
            )
        return user

    # def createUser(self,idx):
    #     #username = 'user' + str(idx)
    #     password = 'User_200' + str(idx)
    #     email = 'user' + str(idx) +'@example.com'
    #     is_active = True
    #     is_staff = False
    #     is_superuser = False
    #
    #     user = User.objects.create_user(password=password, email=email, is_active=is_active, is_staff=is_staff, is_superuser=is_superuser)
    #     user.name = 'Nome ' + str(idx)
    #     user.save()
    #     return user

    def updateProfile(self,user):
        profile = Profile.objects.get(pk=user.id)
        # profile.surname = user.name
        profile.profileVisible = True
        profile.email_verified = True
        profile.save()
