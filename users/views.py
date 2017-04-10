from django.contrib.auth.models import User, Group
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Task
from users.serializers import UserSerializer, GroupSerializer, TaskSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserListView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)


class TaskView(APIView):
    queryset = Task.objects.filter(deleted=False)
    serializer_class = TaskSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    # noinspection PyMethodMayBeStatic
    def get_all_tasks(self, request):
        return TaskSerializer(Task.objects.filter(deleted=False), many=True, context={'user_id': request.user.id}).data

    def get(self, request):
        tasks = self.get_all_tasks(request)
        return Response(tasks)

    def post(self, request):
        serializer = TaskSerializer(data=request.POST, context={'user_id': request.user.id})
        if serializer.is_valid():
            serializer.save()
            tasks = self.get_all_tasks(request)
            return Response(tasks)
        return Response(serializer.errors)

    def update(self, request):
        serializer = TaskSerializer(data=request.POST, context={'user_id': request.user.id})
        if serializer.is_valid():
            serializer.save()
            tasks = self.get_all_tasks(request)
            return Response(tasks)
        return Response(serializer.errors)


class UpdateTaskView(APIView):
    queryset = Task.objects.filter(deleted=False)
    serializer_class = TaskSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    # noinspection PyMethodMayBeStatic
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk, deleted=False)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        task = TaskSerializer(self.get_object(pk), many=False, context={'user_id': request.user.id}).data
        return Response(task)

    def post(self, request, pk):

        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.POST, context={'user_id': request.user.id})
        if serializer.is_valid():
            serializer.save()
            tasks = serializer.data
            return Response(tasks)
        return Response(serializer.errors)

    def delete(self, request, pk):
        task = self.get_object(pk)
        if task:
            task.deleted = True
            task.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
