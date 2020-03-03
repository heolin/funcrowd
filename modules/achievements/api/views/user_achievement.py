# -*- coding: utf-8 -*-
from django.db.models import Q
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from modules.achievements.api.serializers.user_achievement import UserAchievementSerializer
from modules.achievements.consts import Status
from modules.achievements.models import UserAchievement
from tasks.models import Mission, Task


def update_achievements(user_achievements):
    for user_achievement in user_achievements:
        current = user_achievement.value
        user_achievement.update()
        if current != user_achievement.value:
            user_achievement.save()
    return user_achievements


class AchievementsList(GenericAPIView):
    serializer_class = UserAchievementSerializer

    def get(self, request):
        user_achievements = UserAchievement.get_user_achievements(request.user)
        user_achievements = update_achievements(user_achievements)
        serializer = self.serializer_class(user_achievements, many=True)
        return Response(serializer.data)


class UnclosedAchievementsList(GenericAPIView):
    serializer_class = UserAchievementSerializer

    def get(self, request):
        user_achievements = UserAchievement.get_user_achievements(request.user)
        update_achievements(user_achievements)

        user_achievements = UserAchievement.objects.filter(user=request.user, status=Status.FINISHED)
        for a in user_achievements:
            a.close()
        serializer = self.serializer_class(user_achievements, many=True)
        return Response(serializer.data)


class MissionAchievementsList(GenericAPIView):
    serializer_class = UserAchievementSerializer

    def get(self, request, mission_id):
        mission = Mission.objects.filter(id=mission_id).first()
        if mission:
            user_achievements = UserAchievement.get_user_achievements(
                request.user).filter(Q(achievement__mission=mission) | Q(achievement__task__mission=mission))
            user_achievements = update_achievements(user_achievements)

            serializer = self.serializer_class(user_achievements, many=True)

            return Response(serializer.data)
        else:
            raise NotFound("No Mission found for given id.")


class TaskAchievementsList(GenericAPIView):
    serializer_class = UserAchievementSerializer

    def get(self, request, task_id):
        task = Task.objects.filter(id=task_id).first()
        if task:
            user_achievements = UserAchievement.get_user_achievements(
                request.user).filter(achievement__task=task)

            user_achievements = update_achievements(user_achievements)

            serializer = self.serializer_class(user_achievements, many=True)
            return Response(serializer.data)
        else:
            raise NotFound("No Task found for given id.")
