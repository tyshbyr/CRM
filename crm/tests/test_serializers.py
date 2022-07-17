from django.test import TestCase

from crm.models import Client
from crm.serializers import ClientSerializer


class ClientSerializerTests(TestCase):
    def test_expected_data(self):
        object = Client.objects.create(first_name='Bilbo', last_name='Baggins', email='bilbo@baggins.shire', phone='88005553535')
        serializer_data = ClientSerializer(object).data
        expected_data = {
            'id':object.id,
            'first_name':'Bilbo',
            'last_name':'Baggins',
            'email':'bilbo@baggins.shire',
            'phone':'88005553535'
        }
        
        self.assertEqual(serializer_data, expected_data)
        