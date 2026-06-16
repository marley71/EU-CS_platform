from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


class APIRoot(APIView):
    """Central entry point listing all available API endpoints."""

    def get(self, request, format=None):
        data ={
            # Accounts
            #'accounts': reverse('api_accounts', request=request, format=format),
            # Organisations
            'organisations': reverse('api_organisations', request=request, format=format),
            'organisation_types': reverse('organisation_type-list', request=request, format=format),
            # Projects
            'projects': reverse('api_projects', request=request, format=format),
            'activities': reverse('api_activities', request=request, format=format),
            #'project_create': reverse('api_project_create', request=request, format=format),
            'project_topics': reverse('topic-list', request=request, format=format),
            'project_statuses': reverse('status-list', request=request, format=format),
            #'project_hastags': reverse('hastag-list', request=request, format=format),
            #'project_participation_tasks': reverse('participationTask-list', request=request, format=format),
            #'project_geographic_extends': reverse('geographicExtend-list', request=request, format=format),
            # Resources
            'resources': reverse('api_resources', request=request, format=format),
            #'training_resources': reverse('api_training_resources', request=request, format=format),
            #'resource_audiences': reverse('audience-list', request=request, format=format),
            #'resource_themes': reverse('theme-list', request=request, format=format),
            'resource_categories': reverse('category-list', request=request, format=format),
            #'training_resource_education_levels': reverse('educationLevel-list', request=request, format=format),
            #'training_resource_types': reverse('learningResourceType-list', request=request, format=format),
        }
        if request.user.is_authenticated:
            data['accounts'] = reverse('api_accounts', request=request, format=format)
        return Response(data)
