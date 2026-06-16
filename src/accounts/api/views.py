from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from projects.models import Project
from events.models import Event
from organisations.models import Organisation
from resources.models import Resource
from blog.models import Post

from accounts.api.serializers import UserSerializer
from django.conf import settings

User = get_user_model()


class UserList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)


class UserDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, context={'request': request})

        # Normalize host removing trailing slash to avoid double slashes in links
        host = settings.HOST[:-1] if settings.HOST.endswith('/') else settings.HOST

        # Attach lightweight lists of objects created by the user
        created_objects = {
            'projects': [
                {
                    'id': project.id,
                    'name': project.name,
                    'link': host + '/project/' + str(project.id),
                }
                for project in Project.objects.filter(creator=user)
            ],
            'events': [
                {
                    'id': event.id,
                    'title': event.title,
                    'link': event.url,  
                }
                for event in Event.objects.filter(creator=user)
            ],
            'organisations': [
                {
                    'id': organisation.id,
                    'name': organisation.name,
                    'link': host + '/organisation/' + str(organisation.id), 
                }
                for organisation in Organisation.objects.filter(creator=user)
            ],
            'resources': [
                {
                    'id': resource.id,
                    'name': resource.name,
                    'link': host + '/resource/' + str(resource.id), 
                }
                for resource in Resource.objects.filter(creator=user)
            ],
            'posts': [
                {
                    'id': post.id,
                    'title': post.title,
                    'link': host + post.get_absolute_url(),
                }
                for post in Post.objects.filter(author=user)
            ],
        }

        response_data = serializer.data
        response_data.update(created_objects)
        return Response(response_data)
