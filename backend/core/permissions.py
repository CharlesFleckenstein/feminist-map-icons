from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Icon
from .roles import is_contributor, is_moderator


# Anyone may read, only upload-capable roles may write.
# Being signed in is not enough: an account with no role is just a visitor who logged in.
class IsContributorOrReadOnly(BasePermission):
    message = "You need contributor access to submit icons."

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or is_contributor(request.user)


# The per-row half of the icon rules. IsContributorOrReadOnly only answers "may you write
# at all", so the two are used together: that one gates the request, this one gates the row.
class IsOwnerOrModerator(BasePermission):
    # Statuses an author can no longer touch, because a reviewer has signed off on them.
    # Review is the cutoff, not publishing, so content can't be swapped in the gap before
    # an admin publishes. Matches "Delete own unapproved icon" in docs/permissions.md.
    LOCKED_TO_MODERATORS = (Icon.Status.APPROVED, Icon.Status.PUBLISHED)

    message = "You may only change your own icons, and only before they are approved."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if not (user and user.is_authenticated):
            return False
        if is_moderator(user):
            return True

        # Imported rows have no owner, so this comparison fails for them automatically:
        # nobody's id equals None, which is what makes them moderator-only.
        if obj.created_by_id != user.id:
            return False

        return obj.status not in self.LOCKED_TO_MODERATORS


# Gate for the review action. Which statuses a reviewer may set depends on their role and
# is checked in the action itself: moderators get the review outcomes, admins also publish.
class IsReviewer(BasePermission):
    message = "Only moderators and library admins can review submissions."

    def has_permission(self, request, view):
        return is_moderator(request.user)
