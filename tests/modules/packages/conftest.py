import pytest

from modules.order_strategy.models import Strategy
from modules.packages.consts import UserPackageStatus
from modules.packages.models import Package, MissionPackages
from tasks.consts import FINISHED, TaskStatus
from tasks.models import (
    Mission, Task, Item, ItemTemplate, ItemTemplateField
)
from tests.conftest import add_annotation


@pytest.fixture
@pytest.mark.django_db
def task_with_items():
    Strategy.register_values()

    mission = Mission.objects.create(id=1, name="Test mission")
    strategy = Strategy.objects.get(name="StaticStrategyLogic")

    template = ItemTemplate.objects.create(name="task1")
    field = ItemTemplateField.objects.create(name="value", widget="TextLabel")
    template.fields.add(field)
    annotation_field = ItemTemplateField.objects.create(name="output", widget="TextLabel", editable=True)
    template.fields.add(annotation_field)

    packages = MissionPackages.objects.create(mission=mission, strategy=strategy, max_annotations=1)
    package1 = Package.objects.create(parent=packages, order=1)
    package2 = Package.objects.create(parent=packages, order=2)
    package3 = Package.objects.create(parent=packages, order=3)
    package4 = Package.objects.create(parent=packages, order=4)
    package5 = Package.objects.create(parent=packages, order=5, status=FINISHED)

    task1 = Task.objects.create(mission=mission, name="task1", strategy=strategy)
    Item.objects.create(task=task1, template=template, order=1,
                        data={field.name: "task1 item1"}, package=package1)
    Item.objects.create(task=task1, template=template, order=2,
                        data={field.name: "task1 item2"}, package=package2)
    Item.objects.create(task=task1, template=template, order=3,
                        data={field.name: "task1 item3"}, package=package3)
    Item.objects.create(task=task1, template=template, order=4,
                        data={field.name: "task1 item4"}, package=package4)
    Item.objects.create(task=task1, template=template, order=5,
                        data={field.name: "task1 item4"}, package=package5)

    task2 = Task.objects.create(mission=mission, name="task2", strategy=strategy)
    Item.objects.create(task=task2, template=template, order=1,
                        data={field.name: "task2 item1"}, package=package1)
    Item.objects.create(task=task2, template=template, order=2,
                        data={field.name: "task2 item2"}, package=package2)
    Item.objects.create(task=task2, template=template, order=3,
                        data={field.name: "task2 item3"}, package=package3)
    Item.objects.create(task=task2, template=template, order=4,
                        data={field.name: "task2 item4"}, package=package4)


@pytest.fixture
@pytest.mark.django_db
def annotations(task_with_items, user1, user2):
    packages = MissionPackages.objects.first()

    # package with two annotations in all items
    package = packages.packages.all()[0]
    item = package.items.all()[0]
    add_annotation(item, user1)

    item = package.items.all()[1]
    add_annotation(item, user1)

    item = package.items.all()[0]
    add_annotation(item, user2)

    item = package.items.all()[1]
    add_annotation(item, user2)

    # package with one annotation in all items
    package = packages.packages.all()[1]
    item = package.items.all()[0]
    add_annotation(item, user1)

    item = package.items.all()[1]
    add_annotation(item, user1)

    # package with one annotation in one item
    package = packages.packages.all()[2]
    item = package.items.all()[0]
    add_annotation(item, user1)


@pytest.fixture
@pytest.mark.django_db
def packages_with_metadata():
    Strategy.register_values()
    mission = Mission.objects.create(name="Test mission")
    strategy = Strategy.objects.get(name="DepthFirstStrategyLogic")
    task = Task.objects.create(mission=mission, name="task1", strategy=strategy)
    template = ItemTemplate.objects.create(name="task1")
    packages = MissionPackages.objects.create(mission=mission, strategy=strategy, max_annotations=1)

    for order, metadata in enumerate([
        {"country": "Country1", "city": "City1"},
        {"country": "Country1", "city": "City1"},
        {"country": "Country1", "city": "City2"},
        {"country": "Country2", "city": "City3"},
        {"country": "Country2", "city": "City4"},
        {"country": "Country3", "city": "City5"},
    ]):
        package = Package.objects.create(parent=packages, order=order, metadata=metadata)
        for index in range(2):
            Item.objects.create(task=task, template=template, order=order, data={}, package=package)


@pytest.fixture
@pytest.mark.django_db
def annotated_packages_with_status(packages_with_metadata, user1, user2):
    # package 1
    package = Package.objects.all()[0]
    package.status = TaskStatus.FINISHED
    package.save()

    progress = package.get_user_progress(user1)
    progress.status = UserPackageStatus.IN_PROGRESS
    progress.save()

    progress = package.get_user_progress(user2)
    progress.status = UserPackageStatus.FINISHED
    progress.save()

    # package 2
    package = Package.objects.all()[1]
    package.status = TaskStatus.IN_PROGRESS
    package.save()

    progress = package.get_user_progress(user1)
    progress.status = UserPackageStatus.FINISHED
    progress.save()


