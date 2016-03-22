from rest_framework import serializers

from sahem.users.models import User
from .models import Event, Category, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'image', 'slug')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'image')


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ('user', 'content', 'created')


class EventSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    staff = UserSerializer(many=True)
    participant = UserSerializer(many=True)

    comments = CommentSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Event
        fields = (
            'id', 'name', 'category', 'available', 'slug', 'description', 'start', 'end', 'owner', 'staff',
            'participant', 'comments',
            'latitude',
            'longitude', 'created', 'updated')
