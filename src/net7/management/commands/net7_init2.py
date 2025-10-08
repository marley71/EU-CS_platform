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

            # creo il superutente
            self.stdout.write("Creazione superuser")
            call_command('createsuperuser')

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
