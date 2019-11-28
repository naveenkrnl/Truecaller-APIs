from rest_framework import serializers
from django.contrib.auth import get_user_model
from data.models import PersonalContacts
User = get_user_model()

# To display user model search results
class UserModelSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=User
        fields=[
            'uri',
            'name',
            'phone_number',
            'spam_count'
        ]
    def get_uri(self,obj):
        return "http://localhost:8000/api/data/{}/".format(obj.id)

# To display personal_contacts model search results
class PersonalContactsSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=PersonalContacts
        fields=[
            'uri',
            'name',
            'phone_number',
            'spam_count'
        ]
    def get_uri(self,obj):
        return "http://localhost:8000/api/data/p/{}/".format(obj.id)

