from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.users.permissions import IsOwner
from api.users.serializers import (
    UserSerializer, PasswordSerializer, SubscribeSerializer
)
from users.models import User, UserSubscribe


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'id'

    def get_active_user(self):
        return self.request.user

    @action(detail=False, permission_classes=[IsOwner], url_path='me')
    def get_me(self, request):
        if not request.user.is_authenticated:
            return Response(
                'Пожалуйста, авторизуйтесь.',
                status=status.HTTP_401_UNAUTHORIZED
            )
        user = self.get_active_user()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def set_password(self, request):
        user = self.get_active_user()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(
                    serializer.data.get('current_password')
            ):
                return Response(
                    {'current_password': ['Неверный пароль']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def subscribe(self, request, **kwargs):
        user = self.get_active_user()
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        if user == author:
            return Response(
                'Вы не можете подписаться на самого себя.',
                status=status.HTTP_400_BAD_REQUEST
            )
        if UserSubscribe.objects.filter(subscriber=user,
                                        author=author).exists():
            return Response(
                'Вы уже подписаны на этого автора.',
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = SubscribeSerializer(instance=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, **kwargs):
        user = self.get_active_user()
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        subscription = UserSubscribe.objects.filter(
            subscriber=user, author=author
        )
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response('Вы не подписаны на этого пользователя.',
                        status=status.HTTP_400_BAD_REQUEST)
