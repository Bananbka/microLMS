from rest_framework.permissions import BasePermission


class HasPermission(BasePermission):
    message = "You don't have permission to perform this action."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        admin_perms = getattr(view, 'admin_permissions', [])
        if admin_perms and self._has_any_permission(request, admin_perms):
            return True

        if hasattr(view, 'get_required_permissions'):
            required = view.get_required_permissions(request)
        else:
            required = getattr(view, "required_permissions", [])

        if not required:
            return True

        return self._has_all_permissions(request, required)

    def _get_cached_permissions(self, request):
        if not hasattr(request, '_cached_permission_slugs'):
            auth_token = request.auth

            if auth_token and 'permissions' in auth_token:
                request._cached_permission_slugs = set(auth_token['permissions'])
            else:
                request._cached_permission_slugs = set()

        return request._cached_permission_slugs

    def _has_all_permissions(self, request, perms):
        cached = self._get_cached_permissions(request)
        return all(p in cached for p in perms)

    def _has_any_permission(self, request, perms):
        cached = self._get_cached_permissions(request)
        return any(p in cached for p in perms)
