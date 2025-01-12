"""Permission Class for using the REST API."""
#
# ---------------------------------------------------------------------------------------------------------------------
#
from django.http import HttpRequest
from rest_framework import permissions

#
# ---------------------------------------------------------------------------------------------------------------------
#


class UsageAllowed(permissions.BasePermission):  # type: ignore[misc]
    """TODO: Implement Permissions here..."""

    def __init__(self) -> None:
        super().__init__()
        pass

    def has_permission(self, request: HttpRequest) -> bool:
        return True

    pass


#
# ---------------------------------------------------------------------------------------------------------------------
#
