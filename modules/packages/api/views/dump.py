# -*- coding: utf-8 -*-

from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response

from modules.packages.api.views.utils import get_data_dump, create_workbook
from tasks.models import Mission

import pandas as pd


class MissionDumpView(APIView):
    def get(self, request, mission_id, *args, **kwargs):
        mission = Mission.objects.filter(id=mission_id).first()
        if mission:
            data = get_data_dump(mission)
            report = pd.DataFrame(data)
            report_path = create_workbook(report)

            report_file = open(report_path, 'rb')
            response = Response(content=report_file)
            response['Content-Type'] = 'application/pdf'
            response['Content-Disposition'] = f'attachment; filename="report_{mission.id}.xlsx"'
            return response

        raise NotFound("No Mission found for given id.")
