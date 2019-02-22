import modules.statistics as s


def get_agreement_ranking(high_agreement_count):
    stats = s.models.UserStats.objects.all()
    total_count = stats.count()
    position = stats.filter(high_agreement_count__gt=high_agreement_count).count()
    return position, position/total_count


def get_agreement_ranking_mission(mission, high_agreement_count):
    stats = s.models.UserMissionStats.objects.filter(mission=mission)
    total_count = stats.count()
    position = stats.filter(high_agreement_count__gt=high_agreement_count).count()
    return position, position/total_count

