from django.contrib.auth.mixins import AccessMixin


class StaffuserRequiredMixin(AccessMixin):
    """Require that the user is a staff member."""

    permission_denied_message = "You must be a staff user to access this page."

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
