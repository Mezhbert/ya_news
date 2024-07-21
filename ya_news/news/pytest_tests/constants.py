import pytest


COMMENT = 'Текст комментария'
EDITED_COMMENT = 'Обновлённый комментарий'

CLIENT = pytest.lazy_fixture('anon_client')
AUTHOR = pytest.lazy_fixture('auth_client_author')
READER = pytest.lazy_fixture('auth_client_not_author')

URLS = {
    'home': pytest.lazy_fixture('home_url'),
    'detail': pytest.lazy_fixture('detail_url'),
    'login': pytest.lazy_fixture('users_login'),
    'logout': pytest.lazy_fixture('users_logout'),
    'signup': pytest.lazy_fixture('users_signup'),
    'edit': pytest.lazy_fixture('edit_url'),
    'delete': pytest.lazy_fixture('delete_url')
}
