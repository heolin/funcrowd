# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from django.views import View

from modules.packages.api.views.utils import get_data_dump, create_workbook
from tasks.models import Mission

import pandas as pd


class MissionDumpView(View):
    def get(self, request, mission_id, file_name, *args, **kwargs):
        mission = Mission.objects.filter(id=mission_id).first()
        if mission:
            data = get_data_dump(mission)
            report = pd.DataFrame(data)
            report_path = create_workbook(report)

            report_file = open(report_path, 'rb')
            response = HttpResponse(content=report_file)
            response['Content-Type'] = 'application/pdf'
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response

        raise Http404("No Mission found for given id.")
