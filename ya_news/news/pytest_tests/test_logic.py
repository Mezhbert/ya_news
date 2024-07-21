from http import HTTPStatus

from news.models import Comment
from news.forms import BAD_WORDS, WARNING

from .constants import COMMENT, EDITED_COMMENT


def test_anonymous_user_cant_create_comment(client,
                                            detail_url):
    client.post(detail_url, data={'text': COMMENT})
    assert Comment.objects.count() == 0


def test_user_can_create_comment(auth_client_author,
                                 create_news,
                                 detail_url):
    auth_client_author.post(detail_url, data={'text': COMMENT})
    assert Comment.objects.count() == 1
    comment = Comment.objects.first()
    assert comment.text == COMMENT
    assert comment.news == create_news


def test_user_cant_use_bad_words(auth_client_author,
                                 detail_url):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = auth_client_author.post(detail_url, data=bad_words_data)
    assert Comment.objects.count() == 0
    assert WARNING in response.context['form'].errors['text']


def test_author_can_edit_comment(auth_client_author,
                                 create_comment,
                                 edit_url):
    response = auth_client_author.post(edit_url,
                                       data={'text': EDITED_COMMENT})
    create_comment.refresh_from_db()
    assert create_comment.text == EDITED_COMMENT
    assert response.status_code == HTTPStatus.FOUND


def test_user_cant_edit_comment_of_another_user(auth_client_not_author,
                                                create_comment,
                                                edit_url):
    response = auth_client_not_author.post(edit_url,
                                           data={'text': EDITED_COMMENT})
    create_comment.refresh_from_db()
    assert create_comment.text == COMMENT
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_author_can_delete_comment(auth_client_author,
                                   delete_url):
    response = auth_client_author.delete(delete_url)
    assert Comment.objects.count() == 0
    assert response.status_code == HTTPStatus.FOUND


def test_user_cant_delete_comment_of_another_user(auth_client_not_author,
                                                  delete_url):
    response = auth_client_not_author.delete(delete_url)
    assert Comment.objects.count() == 1
    assert response.status_code == HTTPStatus.NOT_FOUND
