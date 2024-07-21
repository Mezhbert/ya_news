from django.conf import settings

from news.forms import CommentForm


def test_news_count(client, create_multiple_news, home_url):
    news_count = client.get(home_url).context['object_list'].count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, create_multiple_news, home_url):
    response = client.get(home_url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, detail_url):
    news = client.get(detail_url).context['news']
    ordered_comments = news.comment_set.order_by('created')
    timestamps = [comment.created for comment in ordered_comments]
    assert timestamps == sorted(timestamps)


def test_anonymous_client_has_no_form(client, detail_url):
    response = client.get(detail_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(auth_client_author, detail_url):
    response = auth_client_author.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
