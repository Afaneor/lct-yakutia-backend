import pytest
from faker import Faker
from rest_framework import status
from rest_framework.reverse import reverse

fake = Faker()


@pytest.mark.django_db()
def test_project_sale_channel_format(
    api_client,
    project_sale_channel,
    project_sale_channel_format,
):
    """Формат ProjectSaleChannel."""
    url = reverse('g-mtg:project-sale-channel-detail', [project_sale_channel.pk])

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response == project_sale_channel_format(project_sale_channel)


@pytest.mark.django_db()
def test_project_sale_channel_post(
    api_client,
):
    """Создание ProjectSaleChannel."""
    url = reverse('g-mtg:project-sale-channel-list')
    response = api_client.post(
        url,
        data={},
        format='json',
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db()
def test_project_sale_channel_delete(api_client, project_sale_channel):
    """Удаление ProjectSaleChannel."""
    url = reverse('g-mtg:project-sale-channel-detail', [project_sale_channel.pk])

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db()
def test_project_sale_channel_change(
    api_client,
    project_sale_channel,
):
    """Изменение ProjectSaleChannel."""
    url = reverse('api:g-mtg:project-sale-channel-detail', [project_sale_channel.pk])

    response = api_client.put(
        url,
        data={},
        format='json',
    )

    assert response.status_code == status.HTTP_200_OK
