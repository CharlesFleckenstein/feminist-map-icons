from django.apps import AppConfig
from django.db.models.signals import post_migrate


def _sync_roles(sender, **kwargs):
    from .roles import sync_roles

    sync_roles()


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        # Keeps the role groups in step with roles.ROLE_PERMISSIONS on every migrate, so
        # a fresh database (and the test database) gets them without anyone doing it by
        # hand. post_migrate because the Permission rows it reads are created by one too.
        post_migrate.connect(_sync_roles, sender=self)
