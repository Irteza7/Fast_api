import pytest
from app import models


@pytest.fixture
def test_vote(session,sample_posts,test_user):
    new_vote = models.Vote(post_id = sample_posts[3].id, user_id = test_user['id'])
    session.add(new_vote)
    session.commit()

def test_vote_on_post(authorized_client, sample_posts):
    res = authorized_client.post("/vote/", json={"post_id":sample_posts[3].id, "dir": 1})
    assert res.status_code == 201

def test_vote_on_post_twice(authorized_client, sample_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id":sample_posts[3].id, "dir": 1})
    assert res.status_code == 409


def test_delete_vote_on_post(authorized_client, sample_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id":sample_posts[3].id, "dir": 0})
    assert res.status_code == 201


def test_delete_vote_not_exist(authorized_client, sample_posts):
    res = authorized_client.post("/vote/", json={"post_id":sample_posts[3].id, "dir": 0})
    assert res.status_code == 404

def test_delete_vote_on_post_not_exist(authorized_client, sample_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": 420, "dir": 1})
    assert res.status_code == 404   

def test_delete_unauth_vote_on_post(client, sample_posts, test_vote):
    res = client.post("/vote/", json={"post_id": sample_posts[3].id, "dir": 1})
    assert res.status_code == 401