import pytest

from tasks.models import Task
from modules.quality_control.models import AgreementMetric
from modules.quality_control.exceptions import MultipleTempaltesFound


@pytest.mark.django_db
def test_one_field(setup_task_one_variable):
    task = Task.objects.first()
    cohens_kappa, _ = AgreementMetric.objects.get_or_create(name="CohensKappaMetric")
    for metric in cohens_kappa.evaluate(task):
        assert metric.name == "CohensKappaMetric"
        assert metric.column == "output"
        assert round(metric.value, 2) == 0.22


@pytest.mark.django_db
def test_high_agreement(setup_task_high_agreement):
    task = Task.objects.first()
    cohens_kappa, _ = AgreementMetric.objects.get_or_create(name="CohensKappaMetric")
    for metric in cohens_kappa.evaluate(task):
        assert metric.name == "CohensKappaMetric"
        assert metric.column == "output"
        assert round(metric.value, 2) == 0.64


@pytest.mark.django_db
def test_multiple_templates(setup_task_multiple_templates):
    task = Task.objects.first()
    cohens_kappa, _ = AgreementMetric.objects.get_or_create(name="CohensKappaMetric")
    with pytest.raises(MultipleTempaltesFound):
        cohens_kappa.evaluate(task)


@pytest.mark.django_db
def test_two_fields(setup_task_two_variables):
    task = Task.objects.first()
    cohens_kappa, _ = AgreementMetric.objects.get_or_create(name="CohensKappaMetric")
    for metric, column in zip(cohens_kappa.evaluate(task), ["output1", "output2"]):
        assert metric.name == "CohensKappaMetric"
        assert metric.column == column
        assert round(metric.value, 2) == 0.22


@pytest.mark.django_db
def test_missing_data(setup_task_missing_data):
    task = Task.objects.first()
    cohens_kappa, _ = AgreementMetric.objects.get_or_create(name="CohensKappaMetric")

    logic = cohens_kappa._logic(task)
    logic.df["output"] = logic.df["data"].apply(lambda x: x["output"])
    counts = logic._get_pivot_table_counts("output")
    assert len(counts) == 9

    for metric in cohens_kappa.evaluate(task):
        assert metric.name == "CohensKappaMetric"
        assert metric.column == "output"
        assert round(metric.value, 2) == 0.19

