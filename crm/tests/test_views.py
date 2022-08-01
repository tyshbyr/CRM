from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from crm.serializers import ClientSerializer
from crm.models import Client, Status

User = get_user_model()

class ClientViewsTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='User1')
        
        self.status1 = Status.objects.create(title='Waiting')
        self.status2 = Status.objects.create(title='In processing')
        self.status3 = Status.objects.create(title='Processed')
        
        self.object1 = Client.objects.create(first_name='Bilbo', last_name='Baggins', email='bilbo@baggins.shire',
                                             phone='88005553535', status=self.status1, manager=self.user1)
        self.object2 = Client.objects.create(first_name='Darth', last_name='Vader',
                                             email='darth@vader.sith', phone='88005553666', status=self.status1)
        self.object3 = Client.objects.create(first_name='Client3', last_name='Simple',
                                             email='client3@simple.com', phone='8999999999', status=self.status3)
        
    
    def test_create_client(self):
        self.client.force_login(self.user1)
        url = reverse('client-list')
        data = {'first_name': 'Frodo', 'last_name':'Baggins', 'email':'frodo@baggins.shire', 'phone':'88005553536'}
        response = self.client.post(url, data, format='json')
        object = Client.objects.get(first_name='Frodo')
        serializer_data = ClientSerializer(object).data
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(object.manager, self.user1)

    def test_retrieve_client(self):
        url = reverse('client-detail', kwargs={'pk':self.object1.pk})
        response = self.client.get(url)
        serializer_data = ClientSerializer(self.object1).data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_client_list(self):
        url = reverse('client-list')
        response = self.client.get(url)
        serializer_data = ClientSerializer((self.object1, self.object2, self.object3), many=True).data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_update_client(self):
        self.client.force_login(self.user1)
        url = reverse('client-detail', kwargs={'pk':self.object1.pk})
        data = {'phone':'89997770707'}
        response = self.client.put(url, data, format='json')
        self.object1.refresh_from_db()
        serializer_data = ClientSerializer(self.object1).data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)
        
    def test_destroy_client(self):
        self.client.force_login(self.user1)
        url = reverse('client-detail', kwargs={'pk':self.object1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_partial_update_client(self):
        self.client.force_login(self.user1)
        url = reverse('client-detail', kwargs={'pk':self.object1.pk})
        data = {'first_name': 'Bob'}
        response = self.client.patch(url, data, format='json') 
        object_update = Client.objects.get(pk=self.object1.pk)
        serializer_data = ClientSerializer(object_update).data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)
        
    def test_filter_client(self):
        url = reverse('client-list')
        response = self.client.get(url, data={'status':self.status1.pk})
        serializer_data = ClientSerializer((self.object1, self.object2), many=True).data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)
        
    def test_search_client(self):
        url = reverse('client-list')
        response = self.client.get(url, data={'search':'Darth'})
        serializer_data = ClientSerializer((self.object2,), many=True).data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)
        
    def test_ordering_client(self):
        url = reverse('client-list')
        response = self.client.get(url, data={'ordering':'-first_name'})
        serializer_data = ClientSerializer((self.object2, self.object3, self.object1), many=True).data
       
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)
 
    def test_update_client_not_manager_not_staff(self):
        self.user2 = User.objects.create(username='User2')
        self.client.force_login(self.user2)
        url = reverse('client-detail', kwargs={'pk':self.object1.pk})
        data = {'phone':'89997770707'}
        response = self.client.put(url, data, format='json')
        self.object1.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.object1.phone, '88005553535')
        
    def test_update_client_user_is_staff(self):
        self.user2 = User.objects.create(username='User2', is_staff=True)
        self.client.force_login(self.user2)
        url = reverse('client-detail', kwargs={'pk':self.object1.pk})
        data = {'phone':'89997770707'}
        response = self.client.put(url, data, format='json')
        self.object1.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.object1.phone, '89997770707')

    def test_destroy_client_not_manager_not_staff(self):
        self.user2 = User.objects.create(username='User2')
        self.client.force_login(self.user2)
        url = reverse('client-detail', kwargs={'pk':self.object1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
