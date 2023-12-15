import pytest
from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory
from faker import Faker
from pytest_factoryboy import register
from rest_framework.fields import DateTimeField
from rest_framework.test import APIClient

from server.apps.g_mtg.models import SaleChannel

fake = Faker()


class SaleChannelFactory(DjangoModelFactory):
    """Фабрика для SaleChannel."""

    class Meta(object):
        model = SaleChannel

    name = factory.LazyAttribute(lambda sale_channel: fake.paragraph())
    key_name = factory.LazyAttribute(lambda sale_channel: fake.paragraph())
    description = factory.LazyAttribute(lambda sale_channel: fake.paragraph())
    projects = factory.SubFactory(__change_me__)


class ProjectUserFactory(DjangoModelFactory):
    """Фабрика для ProjectUser."""

    class Meta(object):
        model = ProjectUser

    project = factory.SubFactory(__change_me__)
    user = factory.SubFactory(__change_me__)


class ProjectSaleChannelFactory(DjangoModelFactory):
    """Фабрика для ProjectSaleChannel."""

    class Meta(object):
        model = ProjectSaleChannel

    projects = factory.SubFactory(__change_me__)
    sale_channel = factory.SubFactory(__change_me__)


class ProjectFactory(DjangoModelFactory):
    """Фабрика для Project."""

    class Meta(object):
        model = Project

    product = factory.SubFactory(__change_me__)
    name = factory.LazyAttribute(lambda project: fake.paragraph())
    description = factory.LazyAttribute(lambda project: fake.paragraph())
    prompt = factory.LazyAttribute(lambda project: fake.paragraph())
    users = factory.SubFactory(__change_me__)


class ProductFactory(DjangoModelFactory):
    """Фабрика для Product."""

    class Meta(object):
        model = Product

    name = factory.LazyAttribute(lambda product: fake.paragraph())
    key_name = factory.LazyAttribute(lambda product: fake.paragraph())
    description = factory.LazyAttribute(lambda product: fake.paragraph())


register(ProductFactory)
register(ProjectFactory)
register(ProjectSaleChannelFactory)
register(ProjectUserFactory)
register(SaleChannelFactory)


@pytest.fixture
def sale_channel_format():
    """Формат SaleChannel."""
    def _sale_channel_format(sale_channel: SaleChannel):
        return {
            'id': sale_channel.pk,
            'name': sale_channel.name,
            'key_name': sale_channel.key_name,
            'description': sale_channel.description,
            'projects': sale_channel.projects,
        }
    return _sale_channel_format


@pytest.fixture
def project_user_format():
    """Формат ProjectUser."""
    def _project_user_format(project_user: ProjectUser):
        return {
            'id': project_user.pk,
            'project': project_user.project,
            'user': project_user.user,
        }
    return _project_user_format


@pytest.fixture
def project_sale_channel_format():
    """Формат ProjectSaleChannel."""
    def _project_sale_channel_format(project_sale_channel: ProjectSaleChannel):
        return {
            'id': project_sale_channel.pk,
            'projects': project_sale_channel.projects,
            'sale_channel': project_sale_channel.sale_channel,
        }
    return _project_sale_channel_format


@pytest.fixture
def project_format():
    """Формат Project."""
    def _project_format(project: Project):
        return {
            'id': project.pk,
            'product': project.product,
            'name': project.name,
            'description': project.description,
            'prompt': project.prompt,
            'users': project.users,
        }
    return _project_format


@pytest.fixture
def product_format():
    """Формат Product."""
    def _product_format(product: Product):
        return {
            'id': product.pk,
            'name': product.name,
            'key_name': product.key_name,
            'description': product.description,
        }
    return _product_format
