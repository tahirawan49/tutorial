from django.contrib.auth.models import User, Group
from rest_framework import serializers

from users.models import Task


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class TaskSerializer(serializers.ModelSerializer):
    my_task = serializers.SerializerMethodField('self_task')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'my_task', 'done']

    def self_task(self, obj):
        user_id = self.context.get("user_id")
        if isinstance(obj, Task) and obj.user.id == user_id:
            return True
        return False

    def create(self, validated_data):
        task_data = validated_data
        user_id = self.context.get("user_id")
        task = Task.objects.create(user_id=user_id, **task_data)
        return task

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.done = validated_data.get('done', instance.done)
        instance.save()
        return instance
