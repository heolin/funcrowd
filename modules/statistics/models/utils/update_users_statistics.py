import modules.statistics as s


def update_user_stats():
    update_user_global_stats()
    update_user_mission_stats()


def update_user_global_stats():
    for stats in s.models.UserStats.objects.all():
        stats.update_high_agreement_count()

    for stats in s.models.UserStats.objects.all():
        stats.update_agreement_ranking()


def update_user_mission_stats():
    for stats in s.models.UserMissionStats.objects.all():
        stats.update_high_agreement_count()

    for stats in s.models.UserMissionStats.objects.all():
        stats.update_agreement_ranking()
