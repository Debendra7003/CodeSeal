from rest_framework import serializers
from .models import Users

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required= True)

    class Meta:
        model = Users
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'image_url', 'resume_link', 'created_time', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = Users.objects.create(**validated_data)
        if password:
            user.set_password(password)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save() 
        return instance
