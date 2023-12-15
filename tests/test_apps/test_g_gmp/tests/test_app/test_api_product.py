import pytest
from faker import Faker
from rest_framework import status
from rest_framework.reverse import reverse

fake = Faker()


@pytest.mark.django_db()
def test_product_format(
    api_client,
    product,
    product_format,
):
    """Формат Product."""
    url = reverse('g-mtg:product-detail', [product.pk])

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response == product_format(product)


@pytest.mark.django_db()
def test_product_post(
    api_client,
):
    """Создание Product."""
    url = reverse('g-mtg:product-list')
    response = api_client.post(
        url,
        data={},
        format='json',
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db()
def test_product_delete(api_client, product):
    """Удаление Product."""
    url = reverse('g-mtg:product-detail', [product.pk])

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db()
def test_product_change(
    api_client,
    product,
):
    """Изменение Product."""
    url = reverse('api:g-mtg:product-detail', [product.pk])

    response = api_client.put(
        url,
        data={},
        format='json',
    )

    assert response.status_code == status.HTTP_200_OK
