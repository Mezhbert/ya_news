import pytest

from http import HTTPStatus

from pytest_django.asserts import assertRedirects

from .constants import CLIENT, AUTHOR, READER, URLS


@pytest.mark.parametrize(
    "urls, users, expected_status",
    [
        (URLS['home'], CLIENT, HTTPStatus.OK),
        (URLS['detail'], CLIENT, HTTPStatus.OK),
        (URLS['login'], CLIENT, HTTPStatus.OK),
        (URLS['logout'], CLIENT, HTTPStatus.OK),
        (URLS['signup'], CLIENT, HTTPStatus.OK),

        (URLS['edit'], AUTHOR, HTTPStatus.OK),
        (URLS['delete'], AUTHOR, HTTPStatus.OK),

        (URLS['edit'], READER, HTTPStatus.NOT_FOUND),
        (URLS['delete'], READER, HTTPStatus.NOT_FOUND),
    ]
)
def test_pages_availability_hitro(urls, users, expected_status):
    response = users.get(urls)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "urls",
    [
        URLS['edit'],
        URLS['delete']
    ]
)
def test_redirect_for_anonymous_client(client, urls, users_login):
    redirect_url = f'{users_login}?next={urls}'
    response = client.get(urls, follow=True)
    assertRedirects(response, redirect_url)
