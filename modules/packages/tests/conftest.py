import pytest

from tasks.consts import FINISHED
from tasks.models import (
    Mission, Task, Item, ItemTemplate, ItemTemplateField, Annotation
)
from users.models import EndWorker

from modules.packages.models import Package, MissionPackages
from modules.order_strategy.models import Strategy


@pytest.fixture
@pytest.mark.django_db
def user1():
    user = EndWorker.objects.create_user("user1@mail.com", "password", username="user")
    return user


@pytest.fixture
@pytest.mark.django_db
def user2():
    user = EndWorker.objects.create_superuser("user2@mail.com", "password", username="user2")
    return user


@pytest.fixture
@pytest.mark.django_db
def db_random():
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('''SELECT setseed(0)''')


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

    packages = MissionPackages.objects.create(mission=mission, strategy=strategy)
    package1 = Package.objects.create(parent=packages, order=1)
    package2 = Package.objects.create(parent=packages, order=2)
    package3 = Package.objects.create(parent=packages, order=3)
    package4 = Package.objects.create(parent=packages, order=4)
    package5 = Package.objects.create(parent=packages, order=5, status=FINISHED)

    task1 = Task.objects.create(mission=mission, name="task1", strategy=strategy)
    task1_item1 = Item.objects.create(task=task1, template=template, order=1,
                    data={field.name: "task1 item1"}, package=package1)
    task1_item2 = Item.objects.create(task=task1, template=template, order=2,
                    data={field.name: "task1 item2"}, package=package2)
    task1_item3 = Item.objects.create(task=task1, template=template, order=3,
                    data={field.name: "task1 item3"}, package=package3)
    task1_item4 = Item.objects.create(task=task1, template=template, order=4,
                    data={field.name: "task1 item4"}, package=package4)
    task1_item5 = Item.objects.create(task=task1, template=template, order=5,
                    data={field.name: "task1 item4"}, package=package5)

    task2 = Task.objects.create(mission=mission, name="task2", strategy=strategy)
    task2_item1 = Item.objects.create(task=task2, template=template, order=1,
                    data={field.name: "task2 item1"}, package=package1)
    task2_item2 = Item.objects.create(task=task2, template=template, order=2,
                    data={field.name: "task2 item2"}, package=package2)
    task2_item3 = Item.objects.create(task=task2, template=template, order=3,
                    data={field.name: "task2 item3"}, package=package3)
    task2_item4 = Item.objects.create(task=task2, template=template, order=4,
                    data={field.name: "task2 item4"}, package=package4)


@pytest.fixture
@pytest.mark.django_db
def annotations(task_with_items, user1, user2):
    packages = MissionPackages.objects.first()

    #paczka z dwoma anotacjami na wszystkich itemach
    package = packages.packages.all()[0]
    item = package.items.all()[0]
    annotation, created = item.get_or_create_annotation(user1)
    annotation.data = {"output": "1"}
    annotation.save()

    item = package.items.all()[1]
    annotation, created = item.get_or_create_annotation(user1)
    annotation.data = {"output": "1"}
    annotation.save()

    item = package.items.all()[0]
    annotation, created = item.get_or_create_annotation(user2)
    annotation.data = {"output": "1"}
    annotation.save()

    item = package.items.all()[1]
    annotation, created = item.get_or_create_annotation(user2)
    annotation.data = {"output": "1"}
    annotation.save()

    # paczka z jedna anotacja na wszystkich itemach

    package = packages.packages.all()[1]
    item = package.items.all()[0]
    annotation, created = item.get_or_create_annotation(user1)
    annotation.data = {"output": "1"}
    annotation.save()

    item = package.items.all()[1]
    annotation, created = item.get_or_create_annotation(user1)
    annotation.data = {"output": "1"}
    annotation.save()

    # paczka z jedna anotacja na jednym itemie

    package = packages.packages.all()[2]
    item = package.items.all()[0]
    annotation, created = item.get_or_create_annotation(user1)
    annotation.data = {"output": "1"}
    annotation.save()


def add_annotation(package, item, user):
    annotation, created = item.get_or_create_annotation(user)
    annotation.data = {"output": "1"}
    annotation.annotated = True
    annotation.save()
