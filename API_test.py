import json

import pytest
import requests

from readConfig import prop_read

class Test_API:
    with open('create_user_request.json', 'r') as file:
        data = json.load(file)
    pytest.new_user_id = ''
    create_json_payload = data
    bearer = prop_read()['token']['bearer']
    base_url = prop_read()['base_url']['url']
    headersAuth = {
        'Authorization': 'Bearer ' + bearer
    }

    def test_create_user(self):
        # to create a new user and check the ID is created
        endpoint = prop_read()['resource']['users']
        response = requests.post(self.base_url + endpoint, json=self.create_json_payload, headers=self.headersAuth)
        assert response.status_code == 201
        response_json = json.loads(response.text)
        assert response_json['id'] is not None
        pytest.new_user_id = response_json['id']
        assert response_json['email'] == self.create_json_payload['email']

    def test_update_username(self):
        # to update the user name of the newly created user
        endpoint = prop_read()['resource']['users'] +"/"+str(pytest.new_user_id)
        update_json_data = {
            "name": "test_update",
            "email": self.create_json_payload['email'],
            "status": self.create_json_payload['status'],
        }
        response = requests.put(self.base_url+endpoint, json= update_json_data, headers=self.headersAuth)
        assert response.status_code == 200
        response_json = json.loads(response.text)
        assert response_json['name']==update_json_data['name']

    def test_create_post(self):
        # To create a new post for the newly created user
        endpoint = prop_read()['resource']['posts']
        create_post_json = {"user_id": pytest.new_user_id, "title": "testhello", "body": "hello hello hello hello"}
        response = requests.post(self.base_url+endpoint, json= create_post_json, headers=self.headersAuth)
        assert response.status_code == 201
        response_json = json.loads(response.text)
        pytest.new_post_id = response_json['id']

    def test_create_comment(self):
        # to create a new comment for the new post created by the new user
        endpoint = prop_read()['resource']['comments']
        create_comments_json = {"post_id":pytest.new_post_id,"name":"Ayushmati Jain PhD","email":"post_comment@eg.io","body":"post comment post comment post comment"}
        response = requests.post(self.base_url+endpoint, json= create_comments_json, headers=self.headersAuth)
        assert response.status_code == 201
        response_json = json.loads(response.text)
        pytest.new_comment_id = response_json['id']

    def test_validate_comment(self):
        # to assert the comment persist to the newly created user
        # retrieve post id from comment get request
        comments_endpoint = prop_read()['resource']['comments']+"/"+str(pytest.new_comment_id)
        response = requests.get(self.base_url + comments_endpoint, headers=self.headersAuth)
        response_json = json.loads(response.text)
        get_post_id = response_json['post_id']

        # retrieve user id from posts get request
        posts_endpoint = prop_read()['resource']['posts'] + "/" + str(get_post_id)
        response = requests.get(self.base_url + posts_endpoint, headers=self.headersAuth)
        response_json = json.loads(response.text)
        get_user_id = response_json['user_id']

        # retrieve user from user get request
        user_endpoint = prop_read()['resource']['users'] + "/" + str(get_user_id)
        response = requests.get(self.base_url + user_endpoint, headers=self.headersAuth)
        response_json = json.loads(response.text)
        get_user_email = response_json['email']
        assert get_user_email == self.create_json_payload['email']

    def test_delete_user(self):
        # to delete the user created and check the resource is no longer accessible
        user_endpoint = prop_read()['resource']['users'] + "/" + str(pytest.new_user_id)
        response = requests.delete(self.base_url + user_endpoint, headers=self.headersAuth)
        assert response.status_code==204
        response = requests.get(self.base_url + user_endpoint, headers=self.headersAuth)
        assert response.status_code==404
        response_json = json.loads(response.text)
        assert response_json['message']=='Resource not found'










