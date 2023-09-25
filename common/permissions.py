from rest_framework.permissions import (
    BasePermission,
    IsAdminUser,
    SAFE_METHODS,
    exceptions,
)
from datetime import datetime, timezone


class IsAdminUserOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return super().has_permission(request=request, view=view)


class IsProductCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.creator != request.user:
            raise exceptions.PermissionDenied("You are not the creator of this product")

        return True


class IsBidder(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.bidder != request.user:
            raise exceptions.PermissionDenied("This bid is not made by you")

        return True


class IsBidProductValid(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.product.valid_till < datetime.now(tz=timezone.utc):
            raise exceptions.PermissionDenied(
                "The product for which this bid was made is not valid now"
            )

        return True
