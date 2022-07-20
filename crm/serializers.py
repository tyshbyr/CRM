from rest_framework import serializers

from .models import Client, Source, Status


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['title']
        
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['title']

class ClientSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)
    source = SourceSerializer(read_only=True)
    
    class Meta:
        model = Client
        fields = '__all__'
