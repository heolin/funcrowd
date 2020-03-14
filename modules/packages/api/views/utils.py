from modules.aggregation.models import ItemAggregation
import xlsxwriter

from modules.packages.api.exceptions import SearchGetParamMalformed

SEPARATOR = "<NEXT>"
EMPTY = "<EMPTY>"
URL = "https://funcrowd-documents.sprawdzamyjakjest.pl/static/pdf/{}.pdf"


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

            if package.metadata:
                for key, value in package.metadata.items():
                    row[key] = value
            data.append(row)
    return data


def create_workbook(report):
    report_path = '/tmp/report.xlsx'

    report['url'] = report['index'].apply(lambda x: URL.format(x))

    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(report_path)
    worksheet = workbook.add_worksheet()

    text_format = workbook.add_format({
        'align': 'left',
        'valign': 'vcenter'})
    text_format.set_text_wrap()

    header_format = workbook.add_format({
        'align': 'center'})
    header_format.set_bold()

    def write_value(column, row, value, rows=1):
        if rows > 1:
            worksheet.merge_range('{}{}:{}{}'.format(column, row, column, row + rows - 1),
                                value, text_format)
        else:
            worksheet.write("{}{}".format(column, row), value, text_format)

    def toColumn(col, offset=4):
        LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        """ Convert given row and column number to an Excel-style cell name. """
        result = []
        col = col + offset
        while col:
            col, rem = divmod(col-1, 26)
            result[:0] = LETTERS[rem]
        return ''.join(result)

    worksheet.write("A1", "Instytucja", header_format)
    worksheet.write("B1", "Dokument", header_format)
    worksheet.write("C1", "URL", header_format)
    worksheet.write("D1", "Status", header_format)

    worksheet.set_column('A:C', 50)
    worksheet.set_column('D:Z', 20)
    for i in range(1, 100):
        worksheet.set_row(i, 20)

    questions = [column for column in list(report) if column.endswith("_answer")]
    questions = sorted(questions, key=lambda x:int(x.split("_")[0]))
    for order in range(len(questions)):
        name = "Pytanie {}".format(order+1) #order_to_task[order+1]
        worksheet.write("{}1".format(toColumn(2*order)), name, header_format)
        worksheet.write("{}1".format(toColumn(2*order+1)), name + "- Pewność", header_format)

    current_row = 2

    for institution, group in report.groupby('institution_slug'):

        _group = group[group['0_answer'] != 'Nie']
        if len(_group) > 0:
            group = _group

        group = group.fillna("")

        start_row = current_row

        for _, data_row in group.iterrows():
            group_start_row = current_row
            max_rows = 0
            for question_index, question in enumerate(questions):
                answers = data_row[question].split(SEPARATOR)
                probs = str(data_row[question+"_prob"]).split(SEPARATOR)
                max_rows = max(max_rows, len(answers))
                for answer_row, values in enumerate(zip(answers, probs)):
                    answer, prob = values
                    write_value(toColumn(question_index*2), current_row + answer_row, answer)
                    write_value(toColumn(question_index*2+1), current_row + answer_row, float(prob))

            current_row += max_rows
            write_value("B", group_start_row, data_row['index'], current_row-group_start_row)
            write_value("C", group_start_row, data_row['url'], current_row-group_start_row)
            write_value("D", group_start_row, data_row['status'], current_row-group_start_row)

        rows = len(group)
        write_value("A", start_row, institution, current_row-start_row)

        current_row += rows - 1

    workbook.close()
    return report_path


def _parse_search_params(search):
    params = search.split(':')
    if len(params) != 2:
        raise ValueError
    return {params[0]: params[1]}


def get_search_query(request):
    search = {}
    if 'search' in request.GET:
        try:
            for params in request.GET["search"].split(','):
                search.update(_parse_search_params(params))
        except ValueError:
            raise SearchGetParamMalformed()
    return search
