from django.core.management.base import BaseCommand
from modules.statistics.models.utils.update_users_statistics import update_user_stats


class Command(BaseCommand):
    help = 'Update users statistics'

    def handle(self, *args, **kwargs):
        update_user_stats()

