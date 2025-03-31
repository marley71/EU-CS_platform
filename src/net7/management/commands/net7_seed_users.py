import csv
import os
from django.core.management.base import BaseCommand,CommandError
from authtools.models import User
from profiles.models import Profile

class Command(BaseCommand):
    help = 'Seed users'

    def handle(self, *args, **kwargs):
        for i in range(1, 4):
            user = self.createUser(i)
            self.updateProfile(user.id)

        self.stdout.write('Database seeded successfully!')


    def createUser(self,idx):
        #username = 'user' + str(idx)
        password = 'User_200' + str(idx)
        email = 'user' + str(idx) +'@example.com'
        is_active = True
        is_staff = False
        is_superuser = False

        user = User.objects.create_user(password=password, email=email, is_active=is_active, is_staff=is_staff, is_superuser=is_superuser)
        user.name = 'Nome ' + str(idx)
        user.save()
        return user

    def updateProfile(self,user_id):
        profile = Profile.objects.get(pk=user_id)
        profile.surname = 'Surname ' + str(user_id)
        profile.profileVisible = True
        profile.save()
