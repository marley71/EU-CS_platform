from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.serializers import UserSerializer


User = get_user_model()


class UserList(APIView):

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)


class UserDetail(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)
