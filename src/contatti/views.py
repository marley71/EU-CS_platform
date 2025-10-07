from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.template.response import TemplateResponse

from .forms import ContattoForm




# Create your views here.

#@login_required(login_url='/login')
def newContact(request):
    #user = request.user
    form = ContattoForm()
    inviato = 0
    if request.method == 'POST':
        form.data = request.POST
        form.save()
        inviato = 1

    #text = get_object_or_404(HelpText, slug='new-project')
    return TemplateResponse(request, 'contatto_form.html', {
        'form': form,'inviato': inviato})


# def showDigests(request):
#
#     return render(request, 'show_digests.html')
#
#
# def showDigest(request, pk, mode='page'):
#     digest = get_object_or_404(Digest, id=pk)
#     info = {"digest": digest, "domain": settings.HOST}
#
#     if(digest.includePosts):
#         posts = Post.objects.filter(
#             status=1,
#             created_on__range=(digest.dateOrg, digest.dateEnd))
#         info["posts"] = posts
#
#     if(digest.includeEvents):
#         events = Event.objects.filter(
#             approved=True,
#             end_date__range=(digest.dateEnd, digest.dateEnd+relativedelta(months=+2)))
#         info["events"] = events
#
#     if(digest.includeOrganisations):
#         organisations = Organisation.objects.filter(
#             dateCreated__range=(digest.dateOrg, digest.dateEnd))
#         info["organisations"] = organisations
#
#     if(digest.includeProjects):
#         projects = Project.objects.filter(
#             approved=True,
#             dateCreated__range=(digest.dateOrg, digest.dateEnd))
#         print(projects.query)
#         info["projects"] = projects
#
#     if(digest.includeResources):
#         resources = Resource.objects.filter(
#             isTrainingResource=False,
#             approved=True,
#             dateUploaded__range=(digest.dateOrg, digest.dateEnd))
#         info["resources"] = resources
#
#     if(digest.includeTrainings):
#         training = Resource.objects.filter(
#             isTrainingResource=True,
#             approved=True,
#             dateUploaded__range=(digest.dateOrg, digest.dateEnd))
#         info["training"] = training
#
#     print(info)
#
#     if mode == 'string':
#         return render_to_string('show_digest.html', info)
#     else:
#         return render(request, 'show_digest.html', info)
