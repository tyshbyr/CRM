from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from crm.serializers import ClientSerializer
from crm.models import Client

class ClientViewsTests(APITestCase):
    def test_create_client(self):
        url = reverse('client-list')
        data = {'first_name': 'Bilbo', 'last_name':'Baggins', 'email':'bilbo@baggins.shire', 'phone':'88005553535'}
        response = self.client.post(url, data, format='json')
        object = Client.objects.get(first_name='Bilbo')
        serializer_data = ClientSerializer(object).data
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer_data)

    def test_retrieve_client(self):
        object = Client.objects.create(first_name='Bilbo', last_name='Baggins', email='bilbo@baggins.shire', phone='88005553535')
        url = reverse('client-detail', kwargs={'pk': object.pk})
        response = self.client.get(url)
        serializer_data = ClientSerializer(object).data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_client_list(self):
        object1 = Client.objects.create(first_name='Bilbo', last_name='Baggins', email='bilbo@baggins.shire', phone='88005553535')
        object2 = Client.objects.create(first_name='Frodo', last_name='Baggins', email='frodo@baggins.shire', phone='88005553536')
        url = reverse('client-list')
        response = self.client.get(url)
        serializer_data = ClientSerializer((object1, object2), many=True).data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_update_client(self):
        object = Client.objects.create(first_name='Bilbo', last_name='Baggins', email='bilbo@baggins.shire', phone='88005553535')
        url = reverse('client-detail', kwargs={'pk': object.pk})
        data = {'phone':'89997770707'}
        response = self.client.put(url, data, format='json')
        object_update = Client.objects.get(pk=object.pk)
        serializer_data = ClientSerializer(object_update).data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)
        
    def test_destroy_client(self):
        object = Client.objects.create(first_name='Bilbo', last_name='Baggins', email='bilbo@baggins.shire', phone='88005553535')
        url = reverse('client-detail', kwargs={'pk': object.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_partial_update_client(self):
        object = Client.objects.create(first_name='Bilbo', last_name='Baggins', email='bilbo@baggins.shire', phone='88005553535')
        url = reverse('client-detail', kwargs={'pk': object.pk})
        data = {'first_name': 'Bob'}
        response = self.client.patch(url, data, format='json') 
        object_update = Client.objects.get(pk=object.pk)
        serializer_data = ClientSerializer(object_update).data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)
        