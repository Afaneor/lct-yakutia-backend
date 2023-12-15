import pytest
from faker import Faker
from rest_framework import status
from rest_framework.reverse import reverse

fake = Faker()


@pytest.mark.django_db()
def test_project_user_format(
    api_client,
    project_user,
    project_user_format,
):
    """Формат ProjectUser."""
    url = reverse('g-mtg:project-user-detail', [project_user.pk])

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response == project_user_format(project_user)


@pytest.mark.django_db()
def test_project_user_post(
    api_client,
):
    """Создание ProjectUser."""
    url = reverse('g-mtg:project-user-list')
    response = api_client.post(
        url,
        data={},
        format='json',
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db()
def test_project_user_delete(api_client, project_user):
    """Удаление ProjectUser."""
    url = reverse('g-mtg:project-user-detail', [project_user.pk])

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db()
def test_project_user_change(
    api_client,
    project_user,
):
    """Изменение ProjectUser."""
    url = reverse('api:g-mtg:project-user-detail', [project_user.pk])

    response = api_client.put(
        url,
        data={},
        format='json',
    )

    assert response.status_code == status.HTTP_200_OK
