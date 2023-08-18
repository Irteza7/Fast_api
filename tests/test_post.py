import json
from app import schemas


def test_get_all_post(authorized_client, sample_posts):
    posts_data = authorized_client.get("/posts/")
    # posts = list(map(lambda x : schemas.PostOut(**x), posts_data.json()))
    # print(posts) 
    assert len(posts_data.json()) == len(sample_posts)
    assert posts_data.status_code == 200

def test_unauth_user_get_all_post(client, sample_posts):
    posts_data = client.get("/posts/")
    assert posts_data.status_code == 401

def test_unauth_user_get_one_post(client, sample_posts):
    posts_data = client.get(f"/posts/{sample_posts[0].id}")
    assert posts_data.status_code == 401

def test_get_one_post(authorized_client, sample_posts):
    post_data = authorized_client.get(f"/posts/{sample_posts[0].id}")
    post = schemas.PostOut(**post_data.json())
    # print(post)
    assert post.Post.id == sample_posts[0].id
    assert post.Post.content == sample_posts[0].content
    assert post.Post.title == sample_posts[0].title
    assert post_data.status_code == 200

def test_create_posts(authorized_client, test_post):
    res = authorized_client.post("/posts/", json=test_post)
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == test_post["title"]
    assert data["content"] == test_post["content"]
    assert "owner_id" in data

def test_unauth_user_create_posts(client, test_post):
    res = client.post("/posts/", json=test_post)
    assert res.status_code == 401

def test_unauth_user_delete_posts(client, sample_posts):
    res = client.delete(f"/posts/{sample_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, sample_posts):
    res = authorized_client.delete(f"/posts/{sample_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_not_found(authorized_client):
    res = authorized_client.delete("/posts/420")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, sample_posts, test_user2):
    res = authorized_client.delete(f"/posts/{sample_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, sample_posts):
    updated_data = {"title":"test update", "content": "updated content", "id": sample_posts[0].id}
    res = authorized_client.put(f"/posts/{sample_posts[1].id}", json=updated_data)
    # print(res.json())
    # assert res.json().get('title') == updated_data["title"]
    post = schemas.Post(**res.json())
    # print(post)
    assert post.title == updated_data["title"]
    assert post.content == updated_data["content"]
    assert res.status_code == 200

def test_update_other_user_post(authorized_client, sample_posts):
    updated_data = {"title":"test update", "content": "updated content", "id": sample_posts[3].id}
    res = authorized_client.put(f"/posts/{sample_posts[3].id}", json=updated_data)
    assert res.status_code == 403

def test_update_unauth_user_post(client, sample_posts):
    updated_data = {"title":"test update", "content": "updated content", "id": sample_posts[0].id}
    res = client.put(f"/posts/{sample_posts[0].id}", json=updated_data)
    assert res.status_code == 401

def test_update_post_not_found(authorized_client, sample_posts):
    updated_data = {"title":"test update", "content": "updated content", "id": sample_posts[0].id}
    res = authorized_client.put("/posts/420", json=updated_data)
    assert res.status_code == 404
