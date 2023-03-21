from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from users.models import User, UserSubscribe


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed',
        )
        extra_kwargs = {
            'email': {'required': True, 'allow_blank': False},
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return UserSubscribe.objects.filter(
            subscriber=user.id, author=obj.id
        ).exists()


class PasswordSerializer(serializers.Serializer):
    """Сериализатор для обновления пароля."""
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)


class SubscribeSerializer(UserSerializer):
    """Сериализатор для подписки на юзеров и просмотра подписчиков."""
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """Это хак, но, поскольку этот сериализатор используется только
         для вьюсетов, в которых залогиненный юзер подписан на автора,
         значение всегда будет True."""
        return True
