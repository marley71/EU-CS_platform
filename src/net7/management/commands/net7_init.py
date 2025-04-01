from django.core.management.base import BaseCommand
from django.core.management import call_command
from eucitizensciencetheme.models import Main, TopBar
from django.db import connection
from projects.models import HelpText,ProjectCountry,Keyword, Topic, HasTag

class Command(BaseCommand):
    help = 'Inizializzazione progetto'

    def handle(self, *args, **options):
        confirmation = input("Sei sicuro di voler procedere? Tutti i dati presenti nel database andranno persi (y/n): [N] ").lower()

        if confirmation == 'y':
            #Chiama il comando migrate
            self.stdout.write("Drop tutte le tabelle...")
            self.drop_tables()

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

            #self.createKeywords()
            #self.createTopics()
            #self.createHasTags()

            self.stdout.write("Comandi eseguiti con successo!")
        else:
            self.stdout.write("Operazione annullata")

    def drop_tables(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                DO $$ DECLARE
                    r RECORD;
                BEGIN
                    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
                        IF r.tablename != 'spatial_ref_sys' THEN
                            EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                        ELSE
                            RAISE NOTICE 'nome è ''spatial_ref_sys'', non eseguo la query';
                        END IF;
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
        # ProjectCountry.objects.create(
        #     country='IT',
        #     country_name='Italy',  # row['Common'],
        #     latitude=42.638426,
        #     longitude=12.674724,
        # )

        pc = ProjectCountry.objects.create(
            country='IT',
            country_name='Abruzzo',  # row['Common'],
            latitude=42.219,
            longitude=13.2357,
        )
        # pc.country_name = 'Abruzzo'
        # pc.save()
        ProjectCountry.objects.create(
            country='IT',
            country_name='Basilicata',  # row['Common'],
            latitude=40.3820,
            longitude=15.4812,
        )
        ProjectCountry.objects.create(
            country='IT',
            country_name='Calabria',  # row['Common'],
            latitude=38.5422,
            longitude=16.3535,
        )
        ProjectCountry.objects.create(
            country='IT',
            country_name='Campania',  # row['Common'],
            latitude=40.5114,
            longitude=14.152,
        )
        ProjectCountry.objects.create(
            country='IT',
            country_name='Emilia Romagna',  # row['Common'],
            latitude=44.2944,
            longitude=11.2048,
        )
        ProjectCountry.objects.create(
            country='IT',
            country_name='Friuli Venezia Giulia',  # row['Common'],
            latitude=45.3858,
            longitude=13.4620,
        )
        ProjectCountry.objects.create(
            country='IT',
            country_name='Lazio',  # row['Common'],
            latitude=41.5427,
            longitude=12.2924,
        )
        ProjectCountry.objects.create(
            country='IT',
            country_name='Liguria',  # row['Common'],
            latitude=44.2417,
            longitude=8.568,
        )
        ProjectCountry.objects.create(
            country='IT',
            country_name='Lombardia',  # row['Common'],
            latitude=45.2757,
            longitude=9.1124,
        )
        ProjectCountry.objects.create(
            country='IT',
            country_name='Marche',  # row['Common'],
            latitude=43.3715,
            longitude=13.3051,
        )
        ProjectCountry.objects.create(
            country='IT',
            country_name='Molise',  # row['Common'],
            latitude=41.3336,
            longitude=14.3937,
        )
        ProjectCountry.objects.create(
            country='IT',
            country_name='Piemonte',  # row['Common'],
            latitude=45.358,
            longitude=7.4056,
        )
        ProjectCountry.objects.create(
            country='IT',
            country_name='Puglia',  # row['Common'],
            latitude=41.745,
            longitude=16.5211,
        )
        ProjectCountry.objects.create(
            country='IT',
            country_name='Sardegna',  # row['Common'],
            latitude=39.137,
            longitude=9.74,
        )
        ProjectCountry.objects.create(
            country='IT',
            country_name='Sicilia',  # row['Common'],
            latitude=38.70,
            longitude=13.2143,
        )
        ProjectCountry.objects.create(
            country='IT',
            country_name='Toscana',  # row['Common'],
            latitude=43.4628,
            longitude=11.1529,
        )
        ProjectCountry.objects.create(
            country='IT',
            country_name='Trentino Alto Adige',  # row['Common'],
            latitude=46.47,
            longitude=11.722,
        )
        ProjectCountry.objects.create(
            country='IT',
            country_name='Umbria',  # row['Common'],
            latitude=43.649,
            longitude=12.2323,
        )
        ProjectCountry.objects.create(
            country='IT',
            country_name='Valle d\'Aosta',  # row['Common'],
            latitude=45.4418,
            longitude=7.1914,
        )
        ProjectCountry.objects.create(
            country='IT',
            country_name='Veneto',  # row['Common'],
            latitude=45.2617,
            longitude=12.1939,
        )






    def createKeywords(self):
        Keyword.objects.create(
            keyword='Importazione',
        )

        Keyword.objects.create(
            keyword='Biodiversità',
        )

        Keyword.objects.create(
            keyword='Genetica',
        )

        Keyword.objects.create(
            keyword='Agrobiodiversità',
        )

        Keyword.objects.create(
            keyword='Turismo',
        )

        Keyword.objects.create(
            keyword='Flora',
        )

        Keyword.objects.create(
            keyword='Fauna',
        )

        Keyword.objects.create(
            keyword='Ambiente',
        )

        Keyword.objects.create(
            keyword='Vino',
        )

    def createTopics(self):
        Topic.objects.create(
            topic='Animali'
        )
        Topic.objects.create(
            topic='Biodiversità'
        )
        Topic.objects.create(
            topic='Biogeografia'
        )
        Topic.objects.create(
            topic='Ecologia & ambiente'
        )
        Topic.objects.create(
            topic='Cultura indigena'
        )
        Topic.objects.create(
            topic='Monitoraggio'
        )
        Topic.objects.create(
            topic='Gestione di risorse naturali'
        )
        Topic.objects.create(
            topic='Monitoraggio specie'
        )
        Topic.objects.create(
            topic='Natura'
        )

    def createHasTags(self):
        HasTag.objects.create(
            hasTag='Apprendimento'
        )
        HasTag.objects.create(
            hasTag='Osservazione'
        )
        HasTag.objects.create(
            hasTag='Identificazione'
        )
        HasTag.objects.create(
            hasTag='Inserimento dati'
        )
        HasTag.objects.create(
            hasTag='Geolocalizazione'
        )
        HasTag.objects.create(
            hasTag='Classificazione'
        )
        HasTag.objects.create(
            hasTag='Etichettatura'
        )