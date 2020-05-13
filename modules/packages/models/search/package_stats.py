import locale
import pandas as pd

from modules.packages.consts import USER_PACKAGE_STATUSES
from modules.packages.models import UserPackageProgress
from tasks.consts import STATUSES
from modules.packages.models.search.packages_search import PackagesSearch


class PackageSearchStatsAggregator(PackagesSearch):
    def __init__(self, mission_packages, search):
        super().__init__(mission_packages, search)

    def get_aggregation(self, user, aggregation_field):
        if self.items.count() == 0:
            return

        df_package_status = self._get_package_status_data(aggregation_field)

        user_statuses = {}
        if user.is_authenticated:
            df_user_status = self._get_user_progress_status_data(user, aggregation_field)
            user_statuses = df_user_status.to_dict(orient='index')

        data = []
        for index, row in df_package_status.iterrows():
            data.append({
                "field": aggregation_field,
                "value": index,
                'package_status': row.to_dict(),
                'user_status': user_statuses.get(index, {}),
                'total': row.sum()
            })
        return data

    def _get_package_status_data(self, aggregation_field):
        # aggregate package status data
        data = self.items.values(f"metadata__{aggregation_field}", "status")
        df = pd.DataFrame(list(data))
        df_package_status = df.groupby(
            f"metadata__{aggregation_field}")['status'].value_counts(
            ).unstack().fillna(0).astype(int)

        for column in STATUSES:
            if column not in df_package_status:
                df_package_status[column] = 0

        df_package_status = df_package_status.loc[
            sorted(df_package_status.index, key=locale.strxfrm)]

        return df_package_status

    def _get_user_progress_status_data(self, user, aggregation_field):
        # aggregate user progress status data
        data = UserPackageProgress.objects.filter(
            user=user, package__in=self.items).values(
            f"package__metadata__{aggregation_field}", 'status', 'package__status')
        df = pd.DataFrame(list(data))
        df_user_status = pd.DataFrame()
        if f"package__metadata__{aggregation_field}" in df:
            df_user_status = df.groupby(
                f"package__metadata__{aggregation_field}")['status'].value_counts(
            ).unstack().fillna(0)

        for column, _ in USER_PACKAGE_STATUSES:
            if column not in df_user_status:
                df_user_status[column] = 0

        df_user_status = df_user_status.loc[
            sorted(df_user_status.index, key=locale.strxfrm)]

        return df_user_status


