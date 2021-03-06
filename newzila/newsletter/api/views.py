from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import NewsletterSerializer, SubscriptionSerializer
from ..models import Newsletter, Subscription


class NewsletterViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = NewsletterSerializer
    queryset = Newsletter.objects.all()
    permission_classes = (AllowAny,)

    # more maintainable but enforces a second query to get instance from pk on SubscriptionSerializer
    lookup_field = 'slug'

    @action(detail=True, methods=["POST"])
    def subscribe(self, request, *args, **kwargs):
        """
        # Subscribe to a newsletter
        ## Example of post data:
        1. Anonymous users:
        ```json
        {
            "email": 'email@example.com'
        }
        ```
        2. Authenticated users, require no data to subscribe.
        """

        _data = {}
        _data.update(request.data)
        # append last to prevent user overriding
        _data.update({
            'newsletter': self.get_object().pk,
            'user': request.user.pk,
        })

        context = self.get_serializer_context()
        serializer = SubscriptionSerializer(data=_data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], url_path='unsubscribe/(?P<email>[-_a-zA-Z0-9@.+~]+)')
    def unsubscribe(self, request, email, *args, **kwargs):
        query_params = {
            'newsletter': self.get_object(),
        }
        if request.user.is_authenticated:
            query_params.update({
                'user': request.user
            })
        else:
            query_params.update({
                'email_field': email,
            })
        subscription = get_object_or_404(
            Subscription, **query_params
        )
        subscription.subscribe_unsubscribe()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], url_path='verify/(?P<token>[^/.]+)')
    def verification(self, request, token, *args, **kwargs):
        """
        Why use slug instead of IDs? since the slugs are more reliable when migrating data
        TODO: provide meaningful 404 errors for different resources
        """
        newsletter = self.get_object()

        subscription = get_object_or_404(
            Subscription, newsletter=newsletter,
            verification_token=token
        )
        subscription.subscribe_verify()
        return Response(status=status.HTTP_200_OK)
