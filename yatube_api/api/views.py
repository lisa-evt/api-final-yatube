"""API views and viewsets for managing blog posts, groups, and comments.

This module provides the DRF endpoints for:
- Full CRUD management of posts with author-level access control.
- Read-only browsing of community groups.
- Nested comment listing, creation, and detail views linked to parent posts.
"""

from django.db.models import QuerySet
from rest_framework import filters, permissions, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.serializers import BaseSerializer

from posts.models import Comment, Follow, Group, Post

from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostRelatedMixin:
    """Mixin for scoping comment queries and actions to a parent post.

    Expects `post_id` in `self.kwargs` from the URL route configuration.
    """

    kwargs: dict

    def get_post(self) -> Post:
        """Retrieve the parent Post object specified by the `post_id` URL.

        Raises:
            KeyError: If `post_id` is not present in URL kwargs.
            Http404: If no post with the given `post_id` exists.
        """
        if 'post_id' not in self.kwargs:
            raise KeyError('post_id not found in kwargs — check URL')
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self) -> QuerySet[Comment]:
        """Return a queryset of comments related to the parent post."""
        return self.get_post().comments.all()


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for managing blog posts.

    Automatically assigns the authenticated request user as the `author`
    on post creation. Updating and deleting are restricted to the post's
    author via `IsAuthorOrReadOnly`.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only ViewSet for groups."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(PostRelatedMixin, viewsets.ModelViewSet):
    """ViewSet for managing comments belonging to a given post.

    Automatically assigns the authenticated request user as the `author`
    on comment creation. Updating and deleting are restricted to the comment's
    author via `IsAuthorOrReadOnly`.
    """

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    lookup_url_kwarg = 'comment_id'

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(CreateModelMixin, ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
