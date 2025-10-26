from django.core.management.base import BaseCommand
from django.core.management import call_command
from eucitizensciencetheme.models import Main, TopBar
from projects.models import HelpText,Keyword, Topic, HasTag
from django.db import connection
from localita.models import Localita
from django.contrib.sites.models import Site
from authtools.models import User

class Command(BaseCommand):
    help = 'Seed dati principali'

    def handle(self, *args, **options):
        self.stdout.write("Svuotamento tabelle")
        self.truncateTables()

        # creo la platform iniziale
        self.stdout.write("Inserimento piattaforma")
        self.createPlatform()

        self.stdout.write("Inserimento dati iniziali di sistema")
        self.createSystemData()

        self.stdout.write("Creazione tab menu")
        self.creaMenuTab()

        self.stdout.write("Load fixiture json")
        self.loadFixiture()

        self.stdout.write("caricamento località")
        self.createCountries()

        self.stdout.write("Eseguo il comando recupero tassonomie ...")
        call_command('net7_fetch_tassonomie')

        self.stdout.write("Eseguo il comando create users ...")
        call_command('net7_seed_users')

        self.stdout.write("Eseguo il comando populate province...")
        call_command('net7_seed_province')

        self.stdout.write("Eseguo il comando populate projects...")
        #call_command('net7_seed_projects',type='normal')
        call_command('net7_seed_projects')

        self.stdout.write("Eseguo il comando populate event...")
        call_command('net7_seed_events')

        self.stdout.write("Eseguo il comando populate blog...")
        call_command('net7_seed_blog')

        self.stdout.write("Eseguo il comando populate pages...")
        call_command('net7_seed_pages')

        self.stdout.write("Comandi eseguiti con successo!")

    def loadFixiture(self):
        call_command('loaddata', './organisations/fixtures/organisation_types.json')
        call_command('loaddata', './projects/fixtures/participationtasks.json')
        call_command('loaddata', './projects/fixtures/status.json')
        # call_command('loaddata', './projects/fixtures/topics.json')
        call_command('loaddata', './projects/fixtures/difficultylevel.json')
        call_command('loaddata', './projects/fixtures/hastag.json')
        call_command('loaddata', './projects/fixtures/geographicextend.json')
        call_command('loaddata', './resources/fixtures/audiences.json')
        call_command('loaddata', './resources/fixtures/themes.json')
        call_command('loaddata', './resources/fixtures/categories.json')

    def createPlatform(self):
        Main.objects.create(
            id=1,
            platform_name="ubuntu",
            platform_description="ubuntu",
        )
        Site.objects.create(
            id=1,
            domain="piattaforma.citizenscience.it",
            name="citizenscience",
        )

    def createSystemData(self):
        HelpText.objects.create(
            id=1,
            title="nuovo progetto",
            title_it="Nuovo progetto/Nuova attività",
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
        TopBar.objects.create(
            name='map',
            slug='/map',
            name_it='Mappa',
            position=4
        )
        TopBar.objects.create(
            name='bdsweek_map',
            slug='/bdsweek_map',
            name_it='BSW',
            position=5
        )
        TopBar.objects.create(
            name='about',
            slug='/p/about',
            name_it='About',
            position=6
        )
        TopBar.objects.create(
            name='risorse_esterne',
            slug='/p/external-resources',
            name_it='Risorse esterne',
            position=7
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

    def truncateTables(self):
        with connection.cursor() as cursor:
            cursor.execute("SET client_min_messages TO NOTICE;")
            cursor.execute("""
                    DO $$ DECLARE
                        stringhe TEXT[] := ARRAY['blog_post', 'contatti_contatto', 'digest_digest',
                    'django_summernote_attachment','easy_thumbnails_source','easy_thumbnails_thumbnail',
                    'easy_thumbnails_thumbnaildimensions','platforms_helptext','platforms_platform_organisation',
                    'eucitizensciencetheme_topbar','pages_pages','platforms_platform',
                    'profiles_profile',
                    'profiles_interestarea',
                    'profiles_profile_organisation',
                    'profiles_profile_interestAreas',
                    'projects_difficultylevel',
                    'projects_hastag',
                    'projects_helptext',
                    'projects_projectcountry',
                    'projects_project_projectCountry',
                    'eucitizensciencetheme_footer',
                    'eucitizensciencetheme_homesection',
                    'eucitizensciencetheme_main',
                    'projects_customfield',
                    'resources_keyword',
                    'projects_fundingbody',
                    'projects_geographicextend',
                    'events_approvedevents',
                    'organisations_organisationpermission',
                    'projects_keyword',
                    'events_helptext',
                    'events_unapprovedevents',
                    'forum_forum',
                    'events_event_organisations',
                    'projects_origindatabase',
                    'projects_participationtask',
                    'forum_conversation_topic_subscribers',
                    'forum_conversation_post',
                    'projects_followedprojects',
                    'projects_project_keywords',
                    'projects_project_customField',
                    'projects_project_organisation',
                    'forum_attachments_attachment',
                    'projects_project_geographicextend',
                    'forum_conversation_topic',
                    'projects_project_participationTask',
                    'projects_project_fundingBody',
                    'projects_project_hasTag',
                    'forum_member_forumprofile',
                    'forum_permission_forumpermission',
                    'projects_project_editors',
                    'projects_follows',
                    'forum_permission_groupforumpermission',
                    'forum_permission_userforumpermission',
                    'projects_likes',
                    'projects_approvedprojects',
                    'events_event',
                    'forum_polls_topicpoll',
                    'forum_polls_topicpolloption',
                    'forum_polls_topicpollvote',
                    'projects_projectpermission',
                    'forum_tracking_forumreadtrack',
                    'forum_tracking_topicreadtrack',
                    'localita_localita',
                    'oauth2_provider_refreshtoken',
                    'oauth2_provider_idtoken',
                    'oauth2_provider_accesstoken',
                    'oauth2_provider_grant',
                    'oauth2_provider_application',
                    'projects_stats',
                    'projects_status',
                    'projects_topic',
                    'projects_project',
                    'projects_project_topic',
                    'oidc_provider_client',
                    'projects_searchstats',
                    'projects_translatedproject',
                    'projects_project_translatedProject',
                    'projects_unapprovedprojects',
                    'oidc_provider_code',
                    'oidc_provider_responsetype',
                    'oidc_provider_client_response_types',
                    'projects_project_provincia',
                    'projects_provincia',
                    'oidc_provider_rsakey',
                    'resources_resource_organisation',
                    'oidc_provider_token',
                    'oidc_provider_userconsent',
                    'organisations_helptext',
                    'organisations_organisation',
                    'resources_audience',
                    'resources_category',
                    'resources_bookmarkedresources',
                    'resources_educationlevel',
                    'resources_helptext',
                    'organisations_organisationtype',
                    'resources_learningresourcetype',
                    'resources_resource',
                    'resources_approvedresources',
                    'resources_resource_keywords',
                    'resources_resource_authors',
                    'resources_resource_audience',
                    'resources_resource_project',
                    'resources_resource_educationLevel',
                    'resources_resource_learningResourceType',
                    'resources_resourcegroup',
                    'resources_resourcepermission',
                    'resources_resourcesgrouped',
                    'resources_savedresources',
                    'resources_theme',
                    'resources_resource_theme',
                    'resources_unapprovedresources',
                    'django_site',
                    'reviews_review',
                    'django_session'];
                        elemento TEXT;
                    BEGIN
                        FOREACH elemento IN ARRAY stringhe
                        LOOP
                            RAISE NOTICE 'Elemento: %', elemento;
                            EXECUTE FORMAT('TRUNCATE TABLE %I RESTART IDENTITY CASCADE', elemento);
                        END LOOP;
                    end $$;
            """)
        User.objects.filter(id__gt=1).delete()