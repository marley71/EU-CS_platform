from django.db.models import Q


def applyProjectsGlobalFilters(request, projects):
    # Approved filters
    if not request.user.is_staff:
        projects = projects.filter(approved=True)
    else:
        if request.GET.get('approved'):
            if request.GET['approved'] == 'approved':
                projects = projects.filter(approved=True)
            elif request.GET['approved'] == 'notApproved':
                projects = projects.filter(approved=False).filter(moderated=True)
            elif request.GET['approved'] == 'notYetModerated':
                projects = projects.filter(moderated=False)
    projects = projects.filter(~Q(hidden=True))
    return projects