from django.core.management.base import BaseCommand
from django.core.management import call_command
from eucitizensciencetheme.models import TopBar
from django.db import connection

class Command(BaseCommand):
    help = 'Seed dati principali'

    def handle(self, *args, **options):
        # Chiama il comando migrate
        #self.stdout.write("Drop tutte le tabelle...")
        #self.drop_tables()

        # self.stdout.write("Eseguo il comando migrate...")
        # call_command('migrate')
        #
        # #creo la platform iniziale
        # self.stdout.write("Inserimento piattaforma")
        # self.createPlatform()
        #
        # # creo la platform iniziale
        # self.stdout.write("Creazione superuser")
        # call_command('createsuperuser')

        # Puoi chiamare altri comandi se necessario
        #self.stdout.write("Eseguo il comando collectstatic...")
        #call_command('collectstatic', verbosity=1, interactive=False)

        #self.stdout.write("Eseguo il comando populate projects...")
        #call_command('populate_projects','../resources/Progetti\ di\ CS.csv', verbosity=1, interactive=False)

        self.stdout.write("Creo menu tab...")
        self.creaMenuTab()

        self.stdout.write("Comandi eseguiti con successo!")

    def creaMenuTab(self):
        self.stdout.write("Creazione menu principali...")
        TopBar.objects.create(
            name='cerca',
            slug = '/projects',
            name_it='Cerca',
            position = 1
        )
        TopBar.objects.create(
            name='blog',
            slug='/blog',
            name_it='Blog',
            position=2
        )
        TopBar.objects.create(
            name='eventi',
            slug='/events',
            name_it='Eventi',
            position=3
        )
        TopBar.objects.create(
            name='map',
            slug='/map',
            name_it='Map',
            position=4
        )
        TopBar.objects.create(
            name='about',
            slug='/about',
            name_it='About',
            position=5
        )