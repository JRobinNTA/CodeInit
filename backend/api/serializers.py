from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserPortfolio, Skill

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('name',)

class UserPortfolioSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserPortfolio
        fields = ('user', 'username', 'year', 'branch', 'skills')
        read_only_fields = ('user', 'username')

    def create(self, validated_data):
        skills_data = validated_data.pop('skills')
        # Get the user from the context
        user = self.context['request'].user
        portfolio = UserPortfolio.objects.create(user=user, **validated_data)

        for skill_data in skills_data:
            skill, _ = Skill.objects.get_or_create(**skill_data)
            portfolio.skills.add(skill)

        return portfolio

    def update(self, instance, validated_data):
        skills_data = validated_data.pop('skills', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if skills_data is not None:
            instance.skills.clear()
            for skill_data in skills_data:
                skill, _ = Skill.objects.get_or_create(**skill_data)
                instance.skills.add(skill)

        instance.save()
        return instance
