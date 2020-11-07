from scipy.stats import entropy
import pandas as pd
import random

from modules.achievements.events import Events
from modules.achievements.models.achievement import Achievement
from tasks.models import UserTaskProgress
from tasks.models import Annotation

from users.consts import ProfileType


GENDERS = ['mężczyzna', 'kobieta']
EDUCATIONS = ['licencjat/inżynierskie', 'wyższe magisterskie',
              'zasadnicze zawodowe', 'średnie', 'gimnazjalne', 'podstawowe']

AGES = ['młody', 'stary', 'dorosły']
PROFILES = [ProfileType.ELEARNING, ProfileType.GAMIFICATION, ProfileType.SERIOUS_GAME]


def _get_gender(row):
    random.seed(row['user_id'] * 2)
    return random.choice(GENDERS)


def _get_age_ranges(age):
    if age <= 22:
        return "młody"
    if age <= 35:
        return "dorosły"
    return "stary"


def _get_best_profile(df, user_id):
    current_row = df[df['user_id'] == user_id].iloc[0]
    df = df[df['user_id'] != user_id]

    # try adding user to each group and check which choice
    values = {}

    for profile in PROFILES:
        current_row['profile'] = profile
        _df = df.append(current_row)
        _probs = _df.groupby(['age', 'edu', 'sex', 'profile']).apply(len) / len(_df)
        _distance = entropy(_probs, base=len(_probs))
        values[profile] = _distance

    values = {k: v for (k, v) in values.items() if v == max(values.values())}
    max_profile = random.choice(list(values.keys()))
    return max_profile


def _get_base():
    _data = []
    for age in AGES:
        for edu in EDUCATIONS:
            for sex in GENDERS:
                for profile in PROFILES:
                    _data.append({
                        "edu": edu,
                        "sex": sex,
                        "age": age,
                        "profile": profile,
                        "user_id": None
                    })

    return pd.DataFrame(_data)


def _get_aggregated_data(task):
    return pd.DataFrame(list(Annotation.objects.filter(
        item__task=task, annotated=True, user_id__gte=2568).values(
        "data__met_1_sex", "data__met_2_age", "data__met_4_education", "user__profile", "user_id")
    ))


def assign_user_profile(task, user):
    df = _get_aggregated_data(task)
    if not len(df):
        return

    # map age to smaller groups
    if 'age' in df:
        df['age'] = df['age'].astype(int).apply(_get_age_ranges)

    # assign sex to missing rows
    if 'sex' in df:
        df.loc[df['sex'] == "nie chcę ujawniać", 'sex'] = \
            df.loc[df['sex'] == "nie chcę ujawniać"].apply(_get_gender, axis=1)

    df = df.append(_get_base(), sort=False)

    # assign profile
    user.profile = _get_best_profile(df, user.id)
    user.save()


class AssignSpaceCalcGroupAchievement(Achievement):
    trigger_events = [
        Events.ON_ITEM_DONE,
        Events.ALWAYS
    ]

    def update(self, user_achievement):
        user_progress = UserTaskProgress.objects.filter(
            user=user_achievement.user, task=self.task).first()
        if user_progress:
            user_achievement.value = user_progress.progress

    def on_close(self, user_achievement):
        user = user_achievement.user
        if user.profile == ProfileType.NORMAL:
            assign_user_profile(self.task, user)

    def save(self, *args, **kwargs):
        if not self.task and not self.mission:
            raise ValueError("Required value for Task and Mission field")
        super(AssignSpaceCalcGroupAchievement, self).save(*args, **kwargs)

