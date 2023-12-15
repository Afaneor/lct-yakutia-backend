import pytest
from faker import Faker
from rest_framework import status
from rest_framework.reverse import reverse

fake = Faker()


@pytest.mark.django_db()
def test_sale_channel_format(
    api_client,
    sale_channel,
    sale_channel_format,
):
    """Формат SaleChannel."""
    url = reverse('g-mtg:sale-channel-detail', [sale_channel.pk])

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response == sale_channel_format(sale_channel)


@pytest.mark.django_db()
def test_sale_channel_post(
    api_client,
):
    """Создание SaleChannel."""
    url = reverse('g-mtg:sale-channel-list')
    response = api_client.post(
        url,
        data={},
        format='json',
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db()
def test_sale_channel_delete(api_client, sale_channel):
    """Удаление SaleChannel."""
    url = reverse('g-mtg:sale-channel-detail', [sale_channel.pk])

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db()
def test_sale_channel_change(
    api_client,
    sale_channel,
):
    """Изменение SaleChannel."""
    url = reverse('api:g-mtg:sale-channel-detail', [sale_channel.pk])

    response = api_client.put(
        url,
        data={},
        format='json',
    )

    assert response.status_code == status.HTTP_200_OK
