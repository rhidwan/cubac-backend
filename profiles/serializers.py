from cgi import test
from rest_framework import serializers

from user.models import User
from profiles.models import EducationalBackground, WorkExperience, AchievementMembership, TestScore, BasicInfo
from user.serializers import UserSerializer


class EducationalBackgroundSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = EducationalBackground
        fields = '__all__'
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class WorkExperienceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = WorkExperience
        fields = '__all__'
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class AchievementMembershipSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = AchievementMembership
        fields = '__all__'
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class TestScoreSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = TestScore
        fields = '__all__'

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class BasicInfoSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = BasicInfo
        fields = '__all__'
        
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
        
class ProfileSerializer(serializers.Serializer):
    basic_info = BasicInfoSerializer(many=True)
    test_scores = TestScoreSerializer(many=True)
    achievements = AchievementMembershipSerializer(many=True)
    work_experiences = WorkExperienceSerializer(many=True)
    educational_backgrounds = EducationalBackgroundSerializer(many=True)
    user=UserSerializer()




