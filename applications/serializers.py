from rest_framework import serializers

from applications.models import Application
from user.models import User

class ApplicationSerializer(serializers.ModelSerializer): 
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('id', 'data', 'roll_no')
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)