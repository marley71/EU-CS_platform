# Standard library imports
from datetime import datetime
import copy
import random

# Third-party imports
from PIL import Image
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils import formats
from django.utils.translation import ugettext_lazy as _

# Local application imports
from platforms.models import Platform
from profiles.models import Profile
from projects.models import Project
from resources.models import Resource
from .forms import OrganisationForm, OrganisationPermissionForm
from .models import HelpText, Organisation, OrganisationPermission, OrganisationType
from localita.models import Localita

from events.models import Event
from eucs_platform.utils import applyProjectsGlobalFilters as applyProjectsGlobalFilters
from resources.views import filter_resources_for_display

User = get_user_model()


@login_required(login_url='/login')
def new_organisation(request):
    user = request.user
    #text = get_object_or_404(HelpText, slug='new-organisation')
    text = "Nuova Organizzazione"
    print("Data submitted", request.POST)


    form = OrganisationForm()
    if request.method == 'POST':
        image_path_database = ''
        form = OrganisationForm(request.POST, request.FILES)
        if form.is_valid():
            # image_path = ''
            # if(request.FILES.get('logo')):
            #     x = form.cleaned_data.get('x')
            #     y = form.cleaned_data.get('y')
            #     w = form.cleaned_data.get('width')
            #     h = form.cleaned_data.get('height')
            #     photo = request.FILES['logo']
            #     image = Image.open(photo)
            #     cropped_image = image.crop((x, y, w+x, h+y))
            #     resized_image = cropped_image.resize((600, 400), Image.LANCZOS)
            #     _datetime = formats.date_format(datetime.now(), 'Y-m-d_hhmmss')
            #     random_num = random.randint(0, 1000)
            #     image_path = "media/images/" + _datetime + '_' + str(random_num) + '_' + photo.name
            #     resized_image.save(image_path)
            #     image_path_database = "images/" + _datetime + '_' + str(random_num) + '_' + photo.name
            images = setImages(request,form)
            saved_organisation = form.save(request, images)
            messages.success(request, _('Organisation added correctly'))
            subject = 'New organisation submitted'
            message = render_to_string('emails/new_organisation.html', {'submitter': user, 'organisationName': saved_organisation.name})
            to = copy.copy(settings.EMAIL_RECIPIENT_LIST)
            to.append(request.user.email)
            from_email = 'admin@citizenscience.it' #settings.EMAIL_FROM_CONTENTS
            email = EmailMessage(subject=subject, body=message, from_email=from_email, to=to)
            email.content_subtype = "html"
            email.send()
            return redirect('/organisation/'+str(saved_organisation.id), {})
        else:
            print(form.errors)

    return TemplateResponse(
            request,
            'organisation_form.html',
            {'form': form, 'user': user, 'text': text})


def setImages(request, form):
    #print('setImages')
    images = []
    post_data = request.POST
    print(post_data)  # Stampa i dati POST nella console
    image1_path = saveImage(request, form, 'logo', 'logo')
    image2_path = saveImage(request, form, 'image1', '1')
    images.append(image1_path)
    images.append(image2_path)
    #print(images)
    return images

def saveImage(request, form, element, ref):
    image_path = ''
    filepath = request.FILES.get(element, False)
    withImage = form.cleaned_data.get('withImage' + ref)
    if (filepath):
        x = form.cleaned_data.get('x_' + ref) if form.cleaned_data.get('x_' + ref) else 0
        y = form.cleaned_data.get('y_' + ref) if form.cleaned_data.get('y_' + ref) else 0
        w = form.cleaned_data.get('width_' + ref) if form.cleaned_data.get('width_' + ref) else 600
        h = form.cleaned_data.get('height_' + ref) if form.cleaned_data.get('height_' + ref) else 400
        print('x ' + str(x) + ' y ' + str(y) + ' w ' + str(w) + ' h ' + str(h))
        photo = request.FILES[element]
        image = Image.open(photo)
        if not image:
            return None

        #cropped_image = image.crop((x, y, w+x, h+y))
        # if (ref == '3'):
        #     finalSize = (1100, 400)
        # else:
        #     finalSize = (600, 400)

        resized_image = image
        # resized_image = cropped_image.resize(finalSize, Image.Resampling.LANCZOS)
        #
        # if (cropped_image.width > image.width):
        #     size = (abs(int(
        #         (finalSize[0]-(finalSize[0]/cropped_image.width*image.width))/2)), finalSize[1])
        #     whitebackground = Image.new(
        #         mode='RGBA', size=size, color=(255, 255, 255, 0))
        #     position = ((finalSize[0] - whitebackground.width), 0)
        #     resized_image.paste(whitebackground, position)
        #     position = (0, 0)
        #     resized_image.paste(whitebackground, position)
        # if (cropped_image.height > image.height):
        #     size = (finalSize[0], abs(
        #         int((finalSize[1]-(finalSize[1]/cropped_image.height*image.height))/2)))
        #     whitebackground = Image.new(
        #         mode='RGBA', size=size, color=(255, 255, 255, 0))
        #     position = (0, (finalSize[1] - whitebackground.height))
        #     resized_image.paste(whitebackground, position)
        #     position = (0, 0)
        #     resized_image.paste(whitebackground, position)

        image_path = saveImageWithPath(resized_image, photo.name)
    elif withImage:
        image_path = '/'
    else:
        image_path = ''

    return image_path


def organisation(request, pk):
    organisation = get_object_or_404(Organisation, id=pk)
    user = request.user
    events = getEvents(pk)
    cooperatorsPK = getCooperators(pk)
    if user != organisation.creator and not user.is_staff and not (user.id in cooperatorsPK):
        editable = False
    else:
        editable = True
    mainProjects = Project.objects.all().filter(mainOrganisation__id=pk)
    associatedProjects = Project.objects.all().filter(organisation__id=pk)
    associatedProjects |= mainProjects
    associatedProjects = associatedProjects.distinct()
    linked_resources = filter_resources_for_display(
        Resource.objects.filter(organisation__id=pk),
        user,
    )
    associatedPlatforms = Platform.objects.all().filter(organisation__id=pk)
    members = Profile.objects.all().filter(profileVisible=True).filter(organisation__id=pk)
    users = getOtherUsers(organisation.creator, members)
    cooperators = getCooperatorsEmail(pk)
    permissionForm = OrganisationPermissionForm(
            initial={'usersCollection': users, 'selectedUsers': cooperators})

    return TemplateResponse(request, 'organisation.html', {
        'organisation': organisation,
        'associatedProjects': associatedProjects,
        'cooperators': cooperatorsPK,
        'linked_resources': linked_resources,
        'associatedPlatforms': associatedPlatforms,
        'members': members,
        'permissionForm': permissionForm,
        'editable': editable,
        'events': events,
        'isSearchPage': True})


def edit_organisation(request, pk):
    organisation = get_object_or_404(Organisation, id=pk)
    user = request.user
    cooperatorsPK = getCooperators(pk)
    if user != organisation.creator and not user.is_staff and not (user.id in cooperatorsPK):
        return redirect('../organisations', {})
    
    initial_data = {
        'name': organisation.name,
        'url': organisation.url,
        'description': organisation.description,
        'orgType': organisation.orgType,
        'logo': organisation.logo,
        'logo_credit' : organisation.logoCredit,
        'withLogo': (True, False)[organisation.logo == ""],
        'contact_point': organisation.contactPoint,
        'contact_point_email': organisation.contactPointEmail,
        'latitude': organisation.latitude,
        'longitude': organisation.longitude,
        'localita': organisation.localita,
    }

    translation_fields = ['description']
    for field in translation_fields:
        for language in settings.MODELTRANSLATION_LANGUAGES:
            initial_data[field + '_' + language] = getattr(organisation, field + '_' + language)

    form = OrganisationForm(initial=initial_data)

    if request.method == 'POST':
        form = OrganisationForm(request.POST, request.FILES)
        if form.is_valid():
            images = setImages(request, form)
            form.save(request, images)
            # --vecchio codice ---
            # image_path = ''
            # if(request.FILES.get('logo')):
            #     x = form.cleaned_data.get('x')
            #     y = form.cleaned_data.get('y')
            #     w = form.cleaned_data.get('width')
            #     h = form.cleaned_data.get('height')
            #     photo = request.FILES['logo']
            #     image = Image.open(photo).convert("RGBA")
            #     cropped_image = image.crop((x, y, w+x, h+y))
            #     resized_image = cropped_image.resize((600, 400), Image.Resampling.LANCZOS)
            #
            #     white_bg = Image.new('RGBA', (600, 400), 'white')
            #     final_image = Image.alpha_composite(white_bg, resized_image)
            #     final_image_rgb = final_image.convert("RGB")
            #     _datetime = formats.date_format(datetime.now(), 'Y-m-d_hhmmss')
            #     random_num = random.randint(0, 1000)
            #     image_path = "media/images/" + _datetime + '_' + str(random_num) + '_' + photo.name
            #     final_image.save(image_path)
            #     image_path_database = "images/" + _datetime + '_' + str(random_num) + '_' + photo.name
            # else:
            #     image_path_database = ''
            # form.save(request, image_path_database)
            return redirect('/organisation/'+str(organisation.id), {})
        else:
            print(form.errors)

    return render(request, 'organisation_form.html', {
        'form': form,
        'organisation': organisation,
        'user': user})


def organisations(request):
    organisations = Organisation.objects.get_queryset().order_by('-dateCreated')
    countriesWithContent = Organisation.objects.all().values_list('country', flat=True).distinct()
    orgTypes = OrganisationType.objects.all()
    totalCount = len(organisations)

    filters = {'keywords': '', 'orgTypes': '', 'country': '', 'orderby': ''}
    """
    if request.GET.get('keywords'):
        organisations = organisations.filter(
                Q(name__icontains=request.GET['keywords'])).distinct()
        filters['keywords'] = request.GET['keywords']
    if request.GET.get('country'):
        organisations = organisations.filter(country=request.GET['country'])
        filters['country'] = request.GET['country']
    if request.GET.get('orgTypes'):
        organisations = organisations.filter(orgType__type=request.GET['orgTypes'])
        filters['orgTypes'] = request.GET['orgTypes']
    if request.GET.get('orderby'):
        filters['orderby'] = request.GET['orderby']        
    """

    localitaids = organisations.values_list(
        'localita_id', flat=True).distinct()
    localita = Localita.objects.filter(id__in=localitaids)


    organisations = applyFilters(request, organisations)
    filters = setFilters(request, filters)
    organisations.distinct()

    counter = len(organisations)

    #To Count
    #For resources count
    allResources = Resource.objects.all()
    if not request.user.is_staff:
        allResources = allResources.filter(approved=True)
    allResources = applyFilters(request, allResources)
    allResources = allResources.distinct()
    resources2 = allResources.filter(~Q(isTrainingResource=True))
    trainingResources = allResources.filter(isTrainingResource=True)
    resourcesCounter = len(resources2)
    trainingResourcesCounter = len(trainingResources)

    #For projects count
    projectsP = Project.objects.all()
    projectsP = applyProjectsGlobalFilters(request, projectsP)
    projectsP = projectsP.filter(~Q(hidden=True)).filter(type='Progetto')
    projectsP = applyFilters(request, projectsP)
    projectsP = projectsP.distinct()
    projectsCounter = len(projectsP)

    projectsA = Project.objects.all()
    projectsA = applyProjectsGlobalFilters(request, projectsA)
    projectsA = projectsA.filter(~Q(hidden=True)).filter(type='Attività')
    projectsA = applyFilters(request, projectsA)
    projectsA = projectsA.distinct()
    attivitaCounter = len(projectsA)


    #For platforms count
    platforms = Platform.objects.all()
    platforms = applyFilters(request, platforms)
    platforms = platforms.distinct()
    platformsCounter = len(platforms)

    #For users count
    users = Profile.objects.all().filter(profileVisible=True).filter(user__is_active=True)
    users = applyFilters(request, users)
    users = users.distinct()
    usersCounter = len(users)

    # Ordering
    if request.GET.get('orderby'):
        if(request.GET.get('orderby') == 'country'):
            organisations = organisations.order_by('country')
        if(request.GET.get('orderby') == 'name'):
            organisations = organisations.order_by('name')    
        else:
            organisations = organisations.order_by('-dateUpdated')
        filters['orderby'] = request.GET['orderby']

    paginator = Paginator(organisations, 18)
    page = request.GET.get('page')
    organisations = paginator.get_page(page)
    localita_selected = None
    if request.GET.get('localita_id'):
        localita_ids = request.GET.getlist('localita_id')
        localitaFound = Localita.objects.filter(id__in=localita_ids)
        localita_selected = ', '.join([item.name for item in localitaFound])

        # localita_selected = Localita.objects.filter(id=request.GET['localita_id']).first()
        # localita_selected = localita_selected.name

    return TemplateResponse(request, 'organisations.html', {
        'organisations': organisations,
        'counter': counter,
        'totalCount': totalCount,
        'organisationsCounter': counter,
        'resourcesCounter': resourcesCounter,
        'trainingResourcesCounter': trainingResourcesCounter,
        'projectsCounter': projectsCounter,
        'attivitaCounter': attivitaCounter,
        'platformsCounter': platformsCounter,
        'usersCounter': usersCounter,
        'filters': filters,
        'countriesWithContent': countriesWithContent,
        'orgTypes': orgTypes,
        'isSearchPage': True,
        'homeSearchCategories': 'organisations',
        'localita': localita,
        'localita_selected': localita_selected,
        'show_search_bar': False})


def delete_organisation(request, pk):
    organisation = get_object_or_404(Organisation, id=pk)
    user = request.user

    if user != organisation.creator and not user.is_staff:
        return redirect('../organisations', {})

    organisation.delete()

    return redirect('../organisations', {})


def organisationsAutocompleteSearch(request):
    if request.GET.get('q'):
        text = request.GET['q']
        organisations = getOrganisationAutocomplete(text)
        organisations = list(organisations)
        return JsonResponse(organisations, safe=False)
    else:
        return HttpResponse("No cookies")


def getOrganisationAutocomplete(text):
    organisations = Organisation.objects.filter(name__icontains=text).values_list('id', 'name').distinct()
    report = []
    for organisation in organisations:
        report.append({"type": "organisation", "id": organisation[0], "text": organisation[1]})
    return report

"""
def preFilteredOrganisations(request):
    organisations = Organisation.objects.get_queryset().order_by('id')
    return applyFilters(request, organisations)


def applyFilters(request, organisations):
    if request.GET.get('country'):
        organisations = organisations.filter(country=request.GET['country'])
    if request.GET.get('orgType'):
        organisations = organisations.filter(orgType=request.GET['orgType'])
    return organisations
"""

def getOtherUsers(creator, members):
    users = []
    for member in members:
        user = get_object_or_404(User, id=member.user_id)
        users.append(user.id)
    users = list(
            User.objects.filter(id__in=users).exclude(
                is_superuser=True).exclude(id=creator.id).values_list('name', 'email'))
    return users


def getCooperators(organisationID):
    users = list(
            OrganisationPermission.objects.all().filter(organisation_id=organisationID).values_list('user', flat=True))
    return users


def getCooperatorsEmail(organisationID):
    users = getCooperators(organisationID)
    cooperators = ""
    for user in users:
        userObj = get_object_or_404(User, id=user)
        cooperators += userObj.email + ", "
    return cooperators


def allowUserOrganisation(request):
    response = {}
    organisationID = request.POST.get("organisation_id")
    users = request.POST.get("users")
    organisation = get_object_or_404(Organisation, id=organisationID)
    if request.user != organisation.creator and not request.user.is_staff:
        # TODO return JsonResponse with error code
        return redirect('../organisations', {})

    # Delete all
    objs = OrganisationPermission.objects.all().filter(organisation_id=organisationID)
    if(objs):
        for obj in objs:
            obj.delete()

    # Insert all
    users = users.split(',')
    for user in users:
        fUser = User.objects.filter(email=user)[:1].get()
        organisationPermission = OrganisationPermission(organisation=organisation, user=fUser)
        organisationPermission.save()

    return JsonResponse(response, safe=False)


def saveImageWithPath(image, photoName):
    _datetime = formats.date_format(datetime.now(), 'Y-m-d_hhmmss')
    random_num = random.randint(0, 1000)
    image_path = "images/" + _datetime + '_' + str(random_num) + '_' + photoName
    image.save('media/' + image_path)
    return image_path

def applyFilters(request, queryset):
    if queryset.model == Project:
        if request.GET.get('keywords'):
            queryset = queryset.filter(
                Q(name__icontains=request.GET['keywords']) |
                Q(keywords__keyword__icontains=request.GET['keywords'])).distinct()
            queryset = queryset.filter(approved=True)

    if queryset.model == Resource:
        if request.GET.get('keywords'):
            queryset = queryset.filter(
                Q(name__icontains=request.GET['keywords']) |
                Q(keywords__keyword__icontains=request.GET['keywords'])).distinct()
            if not request.user.is_staff:
                queryset = queryset.filter(approved=True)

    if queryset.model == Platform:
        if request.GET.get('keywords'):
            keywords = request.GET.get('keywords')
            queryset = queryset.filter(name__icontains=keywords)  

    if queryset.model == Profile:
        if request.GET.get('keywords'):
            keywords = request.GET.get('keywords')
            queryset = queryset.filter(
                Q(user__name__icontains=keywords) |
                Q(interestAreas__interestArea__icontains=keywords) |
                Q(bio__icontains=keywords)).distinct()
            
    if queryset.model == Organisation:
        if request.GET.get('keywords'):
            queryset = queryset.filter(
                Q(name__icontains=request.GET['keywords'])).distinct()
        if request.GET.get('country'):
            queryset = queryset.filter(country=request.GET['country'])
        if request.GET.get('orgTypes'):
            queryset = queryset.filter(orgType__type=request.GET['orgTypes'])

        if request.GET.get('localita_id'):
            localita_ids = request.GET.getlist('localita_id')
            #print("filtro localita_id " + str(localita_ids))
            queryset = queryset.filter(localita_id__in=localita_ids)

    return queryset

def setFilters(request, filters):
    if request.GET.get('keywords'):
        filters['keywords'] = request.GET['keywords']
    if request.GET.get('country'):
        filters['country'] = request.GET['country']
    if request.GET.get('orgTypes'):
        filters['orgTypes'] = request.GET['orgTypes']
    if request.GET.get('orderby'):
        filters['orderby'] = request.GET['orderby']
    if request.GET.get('localita_id'):
        filters['localita_id'] = request.GET.getlist('localita_id')
    return filters

def getEvents(orgID):
    events = list(Event.objects.all().filter(
        mainOrganisation_id=orgID))
    return events