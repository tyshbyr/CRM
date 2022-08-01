from django.test import TestCase

from crm.models import Client, Status, Source
from crm.serializers import ClientSerializer


class ClientSerializerTests(TestCase):
    def test_expected_data(self):
        status = Status.objects.create(title='Waiting')
        source = Source.objects.create(title='AdWords')
        object = Client.objects.create(first_name='Bilbo', last_name='Baggins', email='bilbo@baggins.shire',
                                       comment='Ok', phone='88005553535', status=status, source=source)
        serializer_data = ClientSerializer(object).data
        expected_data = {
            'id':object.id,
            'first_name':'Bilbo',
            'last_name':'Baggins',
            'email':'bilbo@baggins.shire',
            'phone':'88005553535',
            'date_of_creation':serializer_data['date_of_creation'],
            'comment':'Ok',
            'status':{'title':'Waiting'}, 
            'source':{'title':'AdWords'},
            'manager':None
        }
        
        self.assertEqual(serializer_data, expected_data)
        