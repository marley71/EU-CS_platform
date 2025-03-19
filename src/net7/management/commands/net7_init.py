from django.core.management.base import BaseCommand
from django.core.management import call_command
from eucitizensciencetheme.models import Main
from django.db import connection

class Command(BaseCommand):
    help = 'Descrizione del comando personalizzato'

    def handle(self, *args, **options):
        # Chiama il comando migrate
        #self.stdout.write("Drop tutte le tabelle...")
        #self.drop_tables()

        self.stdout.write("Eseguo il comando migrate...")
        call_command('migrate')

        #creo la platform iniziale
        self.stdout.write("Inserimento piattaforma")
        self.createPlatform()

        # creo la platform iniziale
        self.stdout.write("Creazione superuser")
        call_command('createsuperuser')

        # Puoi chiamare altri comandi se necessario
        #self.stdout.write("Eseguo il comando collectstatic...")
        #call_command('collectstatic', verbosity=1, interactive=False)

        self.stdout.write("Eseguo il comando populate projects...")
        call_command('populate_projects', verbosity=1, interactive=False)

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