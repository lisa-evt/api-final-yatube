"""Serializers for converting Post, Group, and Comment models into JSON.

This module handles validation and data transformation for the API:
- PostSerializer: Handles posts, author representation,
    and optional group assignment.
- GroupSerializer: Handles group details.
- CommentSerializer: Handles nested post comments
    and read-only author mappings.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the Post model.

    Exposes the author's username instead of user ID; `group` is optional.
    """

    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for the Group model."""

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model.

    `post` is read-only since it is set automatically by the view layer
    on creation, not supplied by the client.
    """

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'post', 'text', 'author', 'created')
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    def validate(self, attrs):
        if self.context['request'].user == attrs.get('following'):
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return attrs

    class Meta:
        model = Follow
        fields = ('user', 'following')
