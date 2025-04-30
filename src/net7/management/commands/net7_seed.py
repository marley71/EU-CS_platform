from django.core.management.base import BaseCommand
from django.core.management import call_command
from eucitizensciencetheme.models import TopBar
from django.db import connection


class Command(BaseCommand):
    help = 'Seed dati principali'

    def handle(self, *args, **options):
        self.stdout.write("Eseguo il comando create users ...")
        call_command('net7_seed_users')

        self.stdout.write("Eseguo il comando populate province...")
        call_command('net7_seed_province')

        self.stdout.write("Eseguo il comando populate projects...")
        call_command('net7_seed_projects')

        self.stdout.write("Eseguo il comando populate event...")
        call_command('net7_seed_events')

        self.stdout.write("Eseguo il comando populate blog...")
        call_command('net7_seed_blog')

        self.stdout.write("Eseguo il comando populate pages...")
        call_command('net7_seed_pages')

        self.stdout.write("Comandi eseguiti con successo!")

