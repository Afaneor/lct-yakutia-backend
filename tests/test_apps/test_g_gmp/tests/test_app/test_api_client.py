import pytest
from faker import Faker
from rest_framework import status
from rest_framework.reverse import reverse

fake = Faker()


@pytest.mark.django_db()
def test_client_format(
    api_client,
    client,
    client_format,
):
    """Формат Client."""
    url = reverse('g-gmp:client-detail', [client.pk])

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response == client_format(client)


@pytest.mark.django_db()
def test_client_post(
    api_client,
):
    """Создание Client."""
    url = reverse('g-gmp:client-list')
    response = api_client.post(
        url,
        data={},
        format='json',
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db()
def test_client_delete(api_client, client):
    """Удаление Client."""
    url = reverse('g-gmp:client-detail', [client.pk])

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db()
def test_client_change(
    api_client,
    client,
):
    """Изменение Client."""
    url = reverse('api:g-gmp:client-detail', [client.pk])

    response = api_client.put(
        url,
        data={},
        format='json',
    )

    assert response.status_code == status.HTTP_200_OK
