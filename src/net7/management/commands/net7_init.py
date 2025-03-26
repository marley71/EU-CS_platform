from django.core.management.base import BaseCommand
from django.core.management import call_command
from eucitizensciencetheme.models import Main, TopBar
from django.db import connection
from projects.models import HelpText,ProjectCountry

class Command(BaseCommand):
    help = 'Inizializzazione progetto'

    def handle(self, *args, **options):
        # Chiama il comando migrate
        #self.stdout.write("Drop tutte le tabelle...")
        #self.drop_tables()

        self.stdout.write("Eseguo il comando migrate...")
        call_command('migrate')

        # creo la platform iniziale
        self.stdout.write("Creazione superuser")
        call_command('createsuperuser')

        # creo la platform iniziale
        self.stdout.write("Inserimento piattaforma")
        self.createPlatform()

        self.stdout.write("Inserimento dati iniziali di sistema")
        self.createSystemData()

        self.stdout.write("Creazione tab menu")
        self.creaMenuTab()

        # Puoi chiamare altri comandi se necessario
        #self.stdout.write("Eseguo il comando collectstatic...")
        #call_command('collectstatic', verbosity=1, interactive=False)
        call_command('loaddata','./organisations/fixtures/organisation_types.json')
        call_command('loaddata', './projects/fixtures/participationtasks.json')
        call_command('loaddata', './projects/fixtures/status.json')
        call_command('loaddata', './projects/fixtures/topics.json')
        call_command('loaddata', './projects/fixtures/difficultylevel.json')
        call_command('loaddata', './projects/fixtures/hastag.json')
        call_command('loaddata', './projects/fixtures/geographicextend.json')
        call_command('loaddata', './resources/fixtures/audiences.json')
        call_command('loaddata', './resources/fixtures/themes.json')
        call_command('loaddata', './resources/fixtures/categories.json')

        self.createCountries()
        self.createKeywords()

        self.stdout.write("Comandi eseguiti con successo!")

    def drop_tables(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                DO $$ DECLARE
                    r RECORD;
                BEGIN
                    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
                        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                    END LOOP;
                END $$;
            """)
        self.stdout.write('Tutte le tabelle sono state eliminate con successo!')

    def createPlatform(self):
        Main.objects.create(
            id=1,
            platform_name="ubuntu",
            platform_description="ubuntu",
        )

    def createSystemData(self):
        HelpText.objects.create(
            id=1,
            title="nuovo progetto",
            title_it="nuovo progetto",
            paragraph="nuovo progetto",
            paragraph_it="nuovo progetto",
            slug="new-project",
        )

        HelpText.objects.create(
            id=2,
            title="nuovo risorsa training",
            title_it="nuovo risorsa training",
            paragraph="nuovo risorsa training",
            paragraph_it="nuovo risorsa training",
            slug="new-training-resource",
        )

        HelpText.objects.create(
            id=3,
            title="nuovo risorsa",
            title_it="nuovo risorsa",
            paragraph="nuovo risorsa",
            paragraph_it="nuovo risorsa",
            slug="new-resource",
        )

        HelpText.objects.create(
            id=4,
            title="nuova organisation",
            title_it="nuova organisation",
            paragraph="nuova organisation",
            paragraph_it="nuova organisation",
            slug="new-organisation",
        )

        HelpText.objects.create(
            id=5,
            title="nuovo evento",
            title_it="nuovo evento",
            paragraph="nuovo evento",
            paragraph_it="nuovo evento",
            slug="new-event",
        )

        HelpText.objects.create(
            id=6,
            title="nuova piattaforma",
            title_it="nuova piattaforma",
            paragraph="nuova piattaforma",
            paragraph_it="nuova piattaforma",
            slug="new-platform",
        )

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

    def createCountries(self):
        ProjectCountry.objects.create(
            country='IT',
            country_name='Italy',  # row['Common'],
            longitude=42.638426,
            latitude=12.674724,
        )

    def createKeywords(self):
        Keyword.objects.create(
            keyword='Importazione',
        )