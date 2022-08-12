from rest_framework import permissions


class IsAdminOrCreateOnly(permissions.BasePermission):
    """
    If somebody create new user (company owner) return True for POST and False for another methods,
    but if current user is super_admin allow all methods (return True for all methods)
    """
    def has_permission(self, request, view):
        if request.method == 'POST' and request.method == 'GET':
            return True

        return bool(request.user and request.user.is_staff)


class IsCompanyOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        If current user is REGULAR or current user not authenticated return False
        """
        if not request.user.is_anonymous and request.user.user_type == 'ADMIN' or bool(request.user and request.user.is_staff):
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        """
        Check if current user is object owner
        """
        return obj.owner == request.user


class IsCompanyEmployee(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.user_company == obj


class IsProfileOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.pk == request.user.pk or \
                (request.user.user_type == 'ADMIN' and obj.user_company == request.user.user_company):
            return True
        else:
            return False


