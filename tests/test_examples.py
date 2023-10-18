from uuid import UUID

import pytest

create_data_1 = {
    "name": "name1",
    "author": "autor1",
    "address": "addres1"
}


async def test_create_channel_positive(async_client):
    response = await async_client.post("/channel/create", json=create_data_1)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data.get('name') == create_data_1['name']
    assert response_data.get('author') == create_data_1['author']
    assert response_data.get('address') == create_data_1['address']
    uuid_str = response_data.get('id')
    is_valid_uuid = True
    try:
        uuid_obj = UUID(uuid_str)
    except ValueError:
        is_valid_uuid = False
    assert is_valid_uuid


async def test_create_channel_doble_insert(async_client):
    response2 = await async_client.post("/channel/create", json=create_data_1)
    assert response2.status_code == 404


@pytest.mark.parametrize("name, author, address", [
    ("Name1", "Author1", "Address1"),
    ("Name2", "Author2", "Address2"),
    ("Name3", "Author1", "Address3"),
    ("Name4", "Author2", "Address4"),

])
async def test_insert_data(name, author, address, async_client):
    response = await async_client.post("/channel/create", json={'name': name, 'author': author, 'address': address})
    assert response.status_code == 201
    channel = response.json()
    channel_id = channel.get('id')
    response = await async_client.post('/channel/read', json={'id': channel_id})
    assert response.status_code == 200
    data = response.json()
    assert data.get('name') == name
    assert data.get('author') == author
    assert data.get('address') == address
