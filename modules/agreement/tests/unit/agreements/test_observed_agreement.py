import pytest

from tasks.models import Task
from modules.agreement.models import AgreementMetric
from modules.agreement.exceptions import MultipleTempaltesFound


@pytest.mark.django_db
def test_one_field(setup_task_one_variable):
    task = Task.objects.first()
    observed_agreement, _ = AgreementMetric.objects.get_or_create(name="ObservedAgreementMetric")
    for metric in observed_agreement.evaluate(task):
        assert metric.name == "ObservedAgreementMetric"
        assert metric.column == "output"
        assert round(metric.value, 2) == 0.38


@pytest.mark.django_db
def test_high_agreement(setup_task_high_agreement):
    task = Task.objects.first()
    observed_agreement, _ = AgreementMetric.objects.get_or_create(name="ObservedAgreementMetric")
    for metric in observed_agreement.evaluate(task):
        assert metric.name == "ObservedAgreementMetric"
        assert metric.column == "output"
        assert round(metric.value, 2) == 0.72


@pytest.mark.django_db
def test_multiple_templates(setup_task_multiple_templates):
    task = Task.objects.first()
    observed_agreement, _ = AgreementMetric.objects.get_or_create(name="ObservedAgreementMetric")
    with pytest.raises(MultipleTempaltesFound):
        observed_agreement.evaluate(task)


@pytest.mark.django_db
def test_two_fields(setup_task_two_variables):
    task = Task.objects.first()
    observed_agreement, _ = AgreementMetric.objects.get_or_create(name="ObservedAgreementMetric")
    for metric, column in zip(observed_agreement.evaluate(task), ["output1", "output2"]):
        assert metric.name == "ObservedAgreementMetric"
        assert metric.column == column
        assert round(metric.value, 2) == 0.38


@pytest.mark.django_db
def test_missing_data(setup_task_missing_data):
    task = Task.objects.first()
    observed_agreement, _ = AgreementMetric.objects.get_or_create(name="ObservedAgreementMetric")

    logic = observed_agreement._logic(task)
    logic.df["output"] = logic.df["data"].apply(lambda x: x["output"])
    counts = logic._get_pivot_table_counts("output")
    assert len(counts) == 9

    for metric in observed_agreement.evaluate(task):
        assert metric.name == "ObservedAgreementMetric"
        assert metric.column == "output"
        assert round(metric.value, 2) == 0.36


