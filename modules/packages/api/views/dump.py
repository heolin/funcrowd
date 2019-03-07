# -*- coding: utf-8 -*-

from rest_framework.exceptions import NotFound
from rest_pandas import PandasSimpleView

from modules.packages.api.views.utils import get_data_dump
from tasks.models import Mission

import pandas as pd


class MissionDumpView(PandasSimpleView):
    def get_data(self, request, mission_id, *args, **kwargs):
        mission = Mission.objects.filter(id=mission_id).first()
        if mission:
            data = get_data_dump(mission)
            return pd.DataFrame(data)
        raise NotFound("No Task found for given id.")
