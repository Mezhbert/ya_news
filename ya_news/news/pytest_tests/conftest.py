import pytest

from datetime import timedelta

from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

from news.models import Comment, News


@pytest.fixture(autouse=True)
def duto_db(db):
    pass


@pytest.fixture
def anon_client(client):
    return client


@pytest.fixture
def create_users():
    users = {
        'author': User.objects.create_user(username='Лев Толстой'),
        'reader': User.objects.create_user(username='Читатель простой')
    }
    return users


@pytest.fixture
def auth_client_author(client, create_users):
    client.force_login(create_users['author'])
    return client


@pytest.fixture
def auth_client_not_author(client, create_users):
    client.force_login(create_users['reader'])
    return client


@pytest.fixture
def create_news():
    return News.objects.create(title='Заголовок', text='Текст')


@pytest.fixture
def create_multiple_news():
    today = timezone.now()
    news_items = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(news_items)
    return news_items


@pytest.fixture
def create_comment(create_news, create_users):
    return Comment.objects.create(
        news=create_news,
        author=create_users['author'],
        text='Текст комментария'
    )


@pytest.fixture
def create_multiple_comments(create_news, create_users):
    comments = []
    for _ in range(10):
        comment = Comment.objects.create(
            news=create_news,
            author=create_users['author'],
            text='Текст комментария'
        )
        comments.append(comment)
    return comments


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def detail_url(create_news):
    return reverse('news:detail', args=(create_news.pk,))


@pytest.fixture
def users_login():
    return reverse('users:login')


@pytest.fixture
def users_logout():
    return reverse('users:logout')


@pytest.fixture
def users_signup():
    return reverse('users:signup')


@pytest.fixture
def edit_url(create_comment):
    return reverse('news:edit', args=[create_comment.id])


@pytest.fixture
def delete_url(create_comment):
    return reverse('news:delete', args=[create_comment.id])
