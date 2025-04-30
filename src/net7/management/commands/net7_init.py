from django.core.management.base import BaseCommand
from django.core.management import call_command
from eucitizensciencetheme.models import Main, TopBar
from django.db import connection
from projects.models import HelpText,Keyword, Topic, HasTag
from localita.models import Localita

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
            name_it='Notizie',
            position=2
        )
        TopBar.objects.create(
            name='eventi',
            slug='/events',
            name_it='Eventi',
            position=3
        )
#         TopBar.objects.create(
#             name='map',
#             slug='/map',
#             name_it='Mappa',
#             position=4
#         )
        TopBar.objects.create(
            name='bdsweek_map',
            slug='/bdsweek_map',
            name_it='BDS Week',
            position=5
        )
        TopBar.objects.create(
            name='about',
            slug='/p/about',
            name_it='About',
            position=6
        )

    def createCountries(self):
        Localita.objects.create(
            name='Abruzzo',  # row['Common'],
            latitude=42.166259,
            longitude=4.022696,
        )
        Localita.objects.create(
            name='Basilicata',  # row['Common'],
            latitude=40.510071,
            longitude=16.189772,
        )
        Localita.objects.create(
            name='Calabria',  # row['Common'],
            latitude=39.034998,
            longitude=16.485507,
        )
        Localita.objects.create(
            name='Campania',  # row['Common'],
            latitude=40.784588,
            longitude=14.898782,
        )
        Localita.objects.create(
            name='Emilia Romagna',  # row['Common'],
            latitude=44.528254,
            longitude=11.735328,
        )
        Localita.objects.create(
            name='Friuli Venezia Giulia',  # row['Common'],
            latitude=46.048633,
            longitude=13.095477,
        )
        Localita.objects.create(
            name='Lazio',  # row['Common'],
            latitude=41.806455,
            longitude=12.979574,
        )
        Localita.objects.create(
            name='Liguria',  # row['Common'],
            latitude=44.350578,
            longitude=9.338875,
        )
        Localita.objects.create(
            name='Lombardia',  # row['Common'],
            latitude=45.456372,
            longitude=9.529773,
        )
        Localita.objects.create(
            name='Marche',  # row['Common'],
            latitude=43.466468,
            longitude=12.993210,
        )
        Localita.objects.create(
            name='Molise',  # row['Common'],
            latitude=41.602853,
            longitude=14.714702,
        )
        Localita.objects.create(
            name='Piemonte',  # row['Common'],
            latitude=44.910963,
            longitude=7.873050,
        )
        Localita.objects.create(
            name='Puglia',  # row['Common'],
            latitude=40.575244,
            longitude=17.575290,
        )
        Localita.objects.create(
            name='Sardegna',  # row['Common'],
            latitude=39.888745,
            longitude=9.057782,
        )
        Localita.objects.create(
            name='Sicilia',  # row['Common'],
            latitude=37.563651,
            longitude=14.084140,
        )
        Localita.objects.create(
            name='Toscana',  # row['Common'],
            latitude=43.656673,
            longitude=10.883104,
        )
        Localita.objects.create(
            name='Trentino Alto Adige',  # row['Common'],
            latitude=46.022601,
            longitude=11.220584,
        )
        Localita.objects.create(
            name='Umbria',  # row['Common'],
            latitude=43.228488,
            longitude=12.430742,
        )
        Localita.objects.create(
            name='Valle d\'Aosta',  # row['Common'],
            latitude=45.723548,
            longitude=7.334444,
        )
        Localita.objects.create(
            name='Veneto',  # row['Common'],
            latitude=45.547164,
            longitude=11.316033,
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