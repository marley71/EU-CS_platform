import os
import string

from django.views import generic
from datetime import datetime
from django.shortcuts import render
from django.template.response import TemplateResponse
from .models import HomeSection, Main
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q

from projects.models import Project, Likes, Follows, Keyword, Provincia
from resources.models import Resource
from blog.models import Post
from organisations.models import Organisation
from localita.models import Localita
#from provincia.models import Provincia
from platforms.models import Platform
from profiles.models import Profile
from events.models import Event
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from django.conf import settings

from rest_framework import serializers



class ProgettoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'projectGeographicLocation']

# Create your views here, in alphabetical order

def about(request):
    return TemplateResponse(request, 'about.html', {})

def call(request):
    return TemplateResponse(request, 'call.html', {})

def call_ambassadors(request):
    return TemplateResponse(request, 'call_ambassadors.html', {})

def criteria(request):
    return TemplateResponse(request, 'criteria.html',{})

def development(request):
    return TemplateResponse(request, 'development.html',{})

def ecs_project(request):
    return TemplateResponse(request, 'ecs_project.html',{})

def ecs_project_ambassadors(request):
    return TemplateResponse(request, 'ecs_project_ambassadors.html',{})

def ecs_project_codesign(request):
    return TemplateResponse(request, 'ecs_project_codesign.html',{})

def faq(request):
    return TemplateResponse(request, 'faq.html',{})

def final_event(request):
    return TemplateResponse(request, 'final_event.html',{})

def final_launch(request):
    return TemplateResponse(request, 'final_launch.html',{})

def get_projects(request):
    # Filter approved projects with non-null mainOrganisation
    #projects = Project.objects.filter(approved=True).prefetch_related('projectCountry')
    keyword = Keyword.objects.filter(keyword="biodiversity sampling week").first()
    projects = Project.objects.filter(approved=True).exclude(keywords__id = keyword.id).prefetch_related('projectCountry')
    projects_bio = Project.objects.filter(approved=True,keywords__id=keyword.id).prefetch_related('projectCountry')
    markers = []
    markers_bio = []
    zones = [];
    for project in projects:
        # Check if the project has projectCountry related
        # if project.projectCountry.exists():
        #     for country in project.projectCountry.all():
        #         marker = {
        #             'latitude': country.latitude,
        #             'longitude': country.longitude,
        #             'name': project.name,
        #             'project_url': f'/project/{project.id}',
        #             'project_id': project.id
        #         }
        #         markers.append(marker)

        if project.latitude and project.longitude:
            marker = {
                'latitude': project.latitude,
                'longitude': project.longitude,
                'name': project.name,
                'project_url': f'/project/{project.id}',
                'project_id': project.id
            }
            markers.append(marker)

        # if project.aree:
        #     zones.append({
        #         'id': project.id,
        #         'nome': project.name,
        #         'location': project.aree
        #     })

    for project in projects_bio:
        # Check if the project has projectCountry related
        # if project.projectCountry.exists():
        #     for country in project.projectCountry.all():
        #         marker = {
        #             'latitude': country.latitude,
        #             'longitude': country.longitude,
        #             'name': project.name,
        #             'project_url': f'/project/{project.id}',
        #             'project_id': project.id
        #         }
        #         markers.append(marker)

        if project.latitude and project.longitude:
            marker = {
                'latitude': project.latitude,
                'longitude': project.longitude,
                'name': project.name,
                'project_url': f'/project/{project.id}',
                'project_id': project.id
            }
            markers_bio.append(marker)

        # if project.aree:
        #     zones.append({
        #         'id': project.id,
        #         'nome': project.name,
        #         'location': project.aree
        #     })



    #progettiZone = Project.objects.filter(approved=True).exclude(projectGeographicLocation__isnull=True)
    #zones = [{'id': p.id, 'nome': p.name, 'location': p.projectGeographicLocation.geojson} for p in progettiZone]
    #zones = []
    return JsonResponse({'markers': markers, 'zones': zones,'markers_bio': markers_bio})

def get_projects_webmapp(request,type=None):
    geojson = {
        'type': 'FeatureCollection',
        'features': []
    }

    match type:
        case 'progetti-nazionali':
            projectType = 'Progetto'
            projectExtension = ['nazionale','Nazionale','internazionale']
        case 'progetti-regionali':
            projectType = 'Progetto'
            projectExtension = ['regionale','Regionale']
        case 'progetti-locali':
            projectType = 'Progetto'
            projectExtension = ['locale','Comunale','Provinciale']
        case 'attivita-nazionali':
            projectType = 'Attività'
            projectExtension = ['nazionale','Nazionale','internazionale']
        case 'attivita-regionali':
            projectType = 'Attività'
            projectExtension =  ['regionale','Regionale']
        case 'attivita-locali':
            projectType = 'Attività'
            projectExtension = ['locale','Comunale','Provinciale']
        case _:
            projectType = 'Progetto'
            projectExtension = None

    #print("type", type)
    #keyword = Keyword.objects.filter(keyword="biodiversity sampling week").first()
    #projects = Project.objects.filter(approved=True).exclude(keywords__id=keyword.id).prefetch_related('projectCountry')
    projects = Project.objects.filter(approved=True).filter(type=projectType)

    if projectExtension is not None:
        projects = projects.filter(geographicextend__geographicextend__in=projectExtension)

    projects = projects.prefetch_related('projectCountry')

    basedir = os.path.dirname(settings.BASE_DIR)
    html_file = os.path.join(basedir, 'resources', 'template-webmapp.html')
    html_string = ''
    with open(html_file, 'r', encoding='utf-8') as f:
        html_string = f.read()


    for project in projects:
        # Check if the project has projectCountry related
        # if project.projectCountry.exists():
        #     for country in project.projectCountry.all():
        #         marker = {
        #             'latitude': country.latitude,
        #             'longitude': country.longitude,
        #             'name': project.name,
        #             'project_url': f'/project/{project.id}',
        #             'project_id': project.id
        #         }
        #         markers.append(marker)

        image1 = None

        html_string_image = ''
        if project.image1:
            html_file_image = os.path.join(basedir, 'resources', 'template-webmapp-image.html')
            with open(html_file_image, 'r', encoding='utf-8') as f:
                html_string_image = f.read()
            image1 = request.get_host()  + project.image1.url
            html_string_image = html_string_image.replace("{{image1}}", 'https://' + str(image1))

        url = 'https://' + request.get_host() + '/project/' + str(project.id);




        geographicextend = ""
        first = True
        for geo in project.geographicextend.all():
            if first:
                geographicextend += geo.geographicextend
                first = False
            else:
                geographicextend += ' - ' + geo.geographicextend

        variabili_progetto = {
            'nome': project.name,
            'id': project.id,
            'projectlocality': project.projectlocality,
            'url': url,
            'geographicextend' : geographicextend,
            'image' : html_string_image
        }


        html = html_string
        for key, val in variabili_progetto.items():
            html = html.replace(f'{{{{{key}}}}}', str(val))

        # template = string.Template(html_string)
        # html = template.safe_substitute({
        #     'nome' : project.name,
        #     'id' : project.id,
        # })
        geojson['features'].append({
            'type': 'Feature',
            'properties': {
                'id': project.id,
                'popup' : {
                    'html' : html
                }
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [float(project.longitude), float(project.latitude)]
            }
        })

        # if project.latitude and project.longitude:
        #     marker = {
        #         'latitude': project.latitude,
        #         'longitude': project.longitude,
        #         'name': project.name,
        #         'project_url': f'/project/{project.id}',
        #         'project_id': project.id
        #     }
        #     markers.append(marker)

        # if project.aree:
        #     zones.append({
        #         'id': project.id,
        #         'nome': project.name,
        #         'location': project.aree
        #     })
    return JsonResponse(geojson)


def get_organisations(request):
    # Filter approved projects with non-null mainOrganisation
    organisations = Organisation.objects.filter(approved=True)

    # Create a list of marker dictionaries with the required data
    markers = []
    for organisation in organisations:
        #print('localiid' + str(organisation.localita_id))
        #if organisation.localita_id:
        #    localita = Localita.objects.get(id=organisation.localita_id)
        marker = {
            'latitude': organisation.latitude,
            'longitude': organisation.longitude,
            #'latitude': localita.latitude,
            #'longitude': localita.longitude,
            'name': organisation.name,
            'organisation_url': f'/organisation/{organisation.id}',
        }
        markers.append(marker)

    # Return marker data in JSON format
    return JsonResponse({'markers': markers})

def home(request):
    # Projects
    nProjects = 4;
    user = request.user
    main = get_object_or_404(Main)
    projects = Project.objects.get_queryset().filter(~Q(hidden=True)).filter(type='Progetto').filter(approved=True).order_by('-dateCreated')
    projectsCounter = len(projects)
    paginatorprojects = Paginator(projects, nProjects)
    page = request.GET.get('page')
    projects = paginatorprojects.get_page(page)
    # To only show some topics and keywords
    for project in projects:
        combined = list(project.topic.all()) + list(project.keywords.all())
        if len(combined) > nProjects:
            project.display_items = combined[:nProjects]
            project.more_count = len(combined) - nProjects
        else:
            project.display_items = combined
            project.more_count = 0
            
    if user.is_authenticated:
        likes = Likes.objects.filter(user=request.user)
        likes = likes.values_list('project', flat=True)
        follows = Follows.objects.filter(user=request.user)
        follows = follows.values_list('project', flat=True)
    else:
        likes = None
        follows = None

    # Resources
    resources = Resource.objects.all().filter(~Q(isTrainingResource=True)).filter(approved=True).order_by('-dateCreated')
    resources = resources.filter(approved=True)
    resourcesCounter = len(resources)
    paginatorresources = Paginator(resources, 4)
    page = request.GET.get('page')
    resources = paginatorresources.get_page(page)

    # Training Resources
    trainingResources = Resource.objects.all().filter(isTrainingResource=True).filter(approved=True).order_by('-dateCreated')
    trainingResourcesCounter = len(trainingResources)
    paginatorTrainingResources = Paginator(trainingResources, 4)
    page = request.GET.get('page')
    trainingResources = paginatorTrainingResources.get_page(page)

    # Organisations
    organisations = Organisation.objects.all().filter(approved=True).order_by('-dateCreated')
    organisationsCounter = len(organisations)
    paginatororganisation = Paginator(organisations, 4)
    page = request.GET.get('page')
    organisations = paginatororganisation.get_page(page)

    # Platforms
    platforms = Platform.objects.all().filter(approved=True).order_by('-dateCreated')
    platformsCounter = len(platforms)
    paginatorPlatform = Paginator(platforms, 4)
    page = request.GET.get('page')
    platforms = paginatorPlatform.get_page(page)

    # Events
    now = datetime.today()
    now = now.replace(hour=0, minute=0, second=0, microsecond=0)
    events = Event.objects.all().filter(start_date__gt=now).order_by('-featured', 'start_date')
    paginatorEvents = Paginator(events, 3)
    page = request.GET.get('page')
    events = paginatorEvents.get_page(page)

    # Posts
    posts = Post.objects.all().order_by('-created_on')
    posts = posts.filter(status=1)
    postsCounter = len(posts)
    paginatorposts = Paginator(posts, 4)
    page = request.GET.get('page')
    posts = paginatorposts.get_page(page)


    # Users
    usersCounter = Profile.objects.filter(user__is_active=True).count()

    sections = HomeSection.objects.all()

    filters = {
        'keywords': '',
        }

    return TemplateResponse(request, 'home.html', {
        'user': user,
        'main': main,
        'projects': projects,
        'likes': likes,
        'follows': follows,
        'projectsCounter': projectsCounter,
        'resources': resources,
        'resourcesCounter': resourcesCounter,
        'posts': posts,
        'postsCounter': postsCounter,
        'trainingResourcesCounter': trainingResourcesCounter,
        'organisations': organisations,
        'organisationsCounter': organisationsCounter,
        'platforms': platforms,
        'platformsCounter': platformsCounter,
        'usersCounter': usersCounter,
        'events': events,
        'sections': sections,
        'filters': filters,
        'isSearchPage': True})

def imprint(request):
    return TemplateResponse(request, 'pages/imprint.html', {})

def moderation(request):
    return TemplateResponse(request, 'pages/moderation.html', {})

def moderation_quality_criteria(request):
    return TemplateResponse(request, 'pages/moderation_quality_criteria.html', {})

def policy_brief(request):
    return TemplateResponse(request, 'pages/policy_brief.html', {})

def policy_maker_event_2021(request):
    return TemplateResponse(request, 'pages/policy_maker_event_2021.html', {})

def privacy(request):
    return TemplateResponse(request, 'pages/privacy.html', {})

def projects_map(request):
    return TemplateResponse(request, 'pages/map.html', {})

def bdsweek_projects_map(request):

    # user = request.user
    # keyword = Keyword.objects.filter(keyword="biodiversity sampling week").first()
    # projects = Project.objects.filter(approved=True,keywords__id=keyword.id).prefetch_related('projectCountry')
    # projectsCounter = len(projects)
    # # To only show some topics and keywords
    # for project in projects:
    #     combined = list(project.topic.all()) + list(project.keywords.all())
    #     if len(combined) > 3:
    #         project.display_items = combined[:3]
    #         project.more_count = len(combined) - 3
    #     else:
    #         project.display_items = combined
    #         project.more_count = 0


    keyword = Keyword.objects.filter(keyword="biodiversity sampling week").first()
    projects = Project.objects.filter(approved=True,keywords__id=keyword.id).prefetch_related('projectCountry')
    projectsCounter = len(projects)
    # To only show some topics and keywords
    for project in projects:
        combined = list(project.topic.all()) + list(project.keywords.all())
        if len(combined) > 3:
            project.display_items = combined[:3]
            project.more_count = len(combined) - 3
        else:
            project.display_items = combined
            project.more_count = 0

    return TemplateResponse(request, 'pages/bdsweek_map.html', {
        'projects': projects,
        'projectsCounter': projectsCounter,
        })

def subscribe(request):
    return TemplateResponse(request, 'pages/subscribe.html', {})

def terms(request):
    return TemplateResponse(request, 'pages/terms.html', {})

def test(request):
    return TemplateResponse(request, 'base_r2.html', {})

def test2(request):
    return TemplateResponse(request, 'base_r2old.html', {})

def translations(request):
    return TemplateResponse(request, 'pages/translations.html', {})





