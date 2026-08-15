"""Custom permission classes for object-level access control.

This module defines authorization rules used across API endpoints to enforce
ownership restrictions on data operations.
"""
from typing import Any

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Allow read-only access to anyone; writes only for the object's author.

    Note:
        Target model instances must have an `author` attribute
        for this permission check to function properly.
    """

    def has_object_permission(
        self, request: Request, view: APIView, obj: Any
    ) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
