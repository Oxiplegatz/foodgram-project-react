from api.users.permissions import IsOwner
from api.users.serializers import (PasswordSerializer, SubscribeSerializer,
                                   UserSerializer)
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from users.models import User, UserSubscribe


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes_by_action = {
        'create': [AllowAny],
        'list': [IsAuthenticatedOrReadOnly],
        'retrieve': [IsAuthenticatedOrReadOnly]
    }
    lookup_field = 'id'

    def get_active_user(self):
        return self.request.user

    def get_permissions(self):
        try:
            return [permission() for permission in
                    self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

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
        if UserSubscribe.objects.filter(
                subscriber=user, author=author).exists():
            return Response(
                'Вы уже подписаны на этого автора.',
                status=status.HTTP_400_BAD_REQUEST
            )
        UserSubscribe.objects.create(subscriber=user, author=author)
        serializer = SubscribeSerializer(
            instance=author,
            context=self.get_serializer_context()
        )
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
        return Response(
            'Вы не подписаны на этого пользователя.',
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, url_path='subscriptions')
    def get_subscriptions(self, request):
        subscriptions = User.objects.filter(
            subscribers__in=self.request.user.subscriber.all()
        )
        page = self.paginate_queryset(subscriptions)
        serializer = SubscribeSerializer(
            page,
            many=True,
            context=self.get_serializer_context()
        )
        return self.get_paginated_response(serializer.data)
