from modules.aggregation.models import ItemAggregation


def get_data_dump(mission):
    data = []
    for package in mission.packages.packages.all():
        row = {}
        for item in package.items.all():
            aggregation = ItemAggregation.objects.filter(item=item).first()
            if aggregation and aggregation.data:
                for key, value in aggregation.data.items():
                    row["{}_{}".format(item.order, key)] = value
        if row:
            row['index'] = package.name
            row['status'] = package.status
            data.append(row)
    return data
