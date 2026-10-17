import pytest
from apps.accounts.models import User
from rest_framework.test import APIClient
from django.urls import reverse


@pytest.mark.django_db
def test_registration_with_valid_data():
    
    client = APIClient()
    
    url = reverse('register')
    
    response = client.post(url, {'username':'ram', 'email':'ram@gmail.com', 'password':'password', 'password2':'password'})
    
    assert response.status_code == 201
    assert User.objects.count() == 1
    assert response.data['data']['username'] == 'ram'
    assert 'password' not in response.data
    
@pytest.mark.django_db
def test_duplicate_email_is_not_registered():
    
    client = APIClient()
    
    url = reverse('register')
    first_response = client.post(url, {'username':'hari', 'email':'ram@gmail.com', 'password':'password', 'password2':'password'})
    response = client.post(url, {'username':'ram', 'email':'ram@gmail.com', 'password':'password', 'password2':'password'})
    
    assert response.status_code == 400
    assert User.objects.count() == 1
    assert first_response.status_code == 201
    assert 'email' in response.data
    

@pytest.mark.django_db
def test_registration_with_mismatched_password_doesnot_create_user():
    
    client = APIClient()
    
    url = reverse('register')
    
    response = client.post(url, {'username':'ram', 'email':'ram@gmail.com', 'password':'password1', 'password2':'password'})
    
    assert response.status_code == 400
    assert User.objects.count() == 0
    

@pytest.mark.django_db
def test_login_with_incorrect_credentials():

    User.objects.create_user(username='username', email='ram@gmail.com', password='password')

    client = APIClient()
    url = reverse('login')
    
    response = client.post(url, {'email':'ram@gmail.com', 'password':'password1'})
    
    assert response.status_code == 400
    assert "access" not in response.data
    assert "non_field_errors" in response.data
    

@pytest.mark.django_db
def test_login_with_correct_credentials():

    User.objects.create_user(username='username', email='ram@gmail.com', password='password')

    client = APIClient()
    url = reverse('login')
    
    response = client.post(url, {'email':'ram@gmail.com', 'password':'password'})
    
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_jwt_credentials():

    User.objects.create_user(username='username', email='ram@gmail.com', password='password')
    hari = User.objects.create_user(username='hari', email='hari@gmail.com', password='password')

    client = APIClient()
    url = reverse('login')
    
    login_response = client.post(url, {'email':'ram@gmail.com', 'password':'password'})

    access_token = login_response.data['access']
    
    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access_token}"
    )
    
    search_response = client.get(reverse('users'), {'q':'hari'})
    
    assert search_response.status_code == 200
    assert len(search_response.data) == 1
    assert search_response.data[0]['email'] == hari.email