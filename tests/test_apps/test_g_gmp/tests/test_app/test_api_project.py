import pytest
from faker import Faker
from rest_framework import status
from rest_framework.reverse import reverse

fake = Faker()


@pytest.mark.django_db()
def test_project_format(
    api_client,
    project,
    project_format,
):
    """Формат Project."""
    url = reverse('g-gmp:project-detail', [project.pk])

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response == project_format(project)


@pytest.mark.django_db()
def test_project_post(
    api_client,
):
    """Создание Project."""
    url = reverse('g-gmp:project-list')
    response = api_client.post(
        url,
        data={},
        format='json',
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db()
def test_project_delete(api_client, project):
    """Удаление Project."""
    url = reverse('g-gmp:project-detail', [project.pk])

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db()
def test_project_change(
    api_client,
    project,
):
    """Изменение Project."""
    url = reverse('api:g-gmp:project-detail', [project.pk])

    response = api_client.put(
        url,
        data={},
        format='json',
    )

    assert response.status_code == status.HTTP_200_OK
