import pytest
from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory
from faker import Faker
from pytest_factoryboy import register
from rest_framework.fields import DateTimeField
from rest_framework.test import APIClient

from server.apps.g_mtg.models import Client

fake = Faker()


class ClientFactory(DjangoModelFactory):
    """Фабрика для Client."""

    class Meta(object):
        model = Client

    external_key = factory.LazyAttribute(lambda client: fake.paragraph())
    data_source = factory.LazyAttribute(lambda client: fake.paragraph())
    type = factory.LazyAttribute(lambda client: fake.paragraph())


class ProjectFactory(DjangoModelFactory):
    """Фабрика для Project."""

    class Meta(object):
        model = Project

    user = factory.SubFactory(__change_me__)
    product = factory.SubFactory(__change_me__)
    name = factory.LazyAttribute(lambda project: fake.paragraph())
    description = factory.LazyAttribute(lambda project: fake.paragraph())
    prompt = factory.LazyAttribute(lambda project: fake.paragraph())


class ProductFactory(DjangoModelFactory):
    """Фабрика для Product."""

    class Meta(object):
        model = Product

    name = factory.LazyAttribute(lambda product: fake.paragraph())
    description = factory.LazyAttribute(lambda product: fake.paragraph())


register(ProductFactory)
register(ProjectFactory)
register(ClientFactory)


@pytest.fixture
def client_format():
    """Формат Client."""
    def _client_format(client: Client):
        return {
            'id': client.pk,
            'external_key': client.external_key,
            'data_source': client.data_source,
            'client_type': client.type,
        }
    return _client_format


@pytest.fixture
def project_format():
    """Формат Project."""
    def _project_format(project: Project):
        return {
            'id': project.pk,
            'user': project.user,
            'product': project.product,
            'name': project.name,
            'description': project.description,
            'prompt': project.prompt,
        }
    return _project_format


@pytest.fixture
def product_format():
    """Формат Product."""
    def _product_format(product: Product):
        return {
            'id': product.pk,
            'name': product.name,
            'description': product.description,
        }
    return _product_format
