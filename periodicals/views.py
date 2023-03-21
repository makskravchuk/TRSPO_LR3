from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from periodicals.models import User, Magazine, Subscription, Payment
from periodicals.serializers import UserSerializer, MagazineSerializer, SubscriptionSerializer, PaymentSerializer, \
    EditionChoiceSerializer


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserAPIView(APIView):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(data=serializer.data)

    def post(self, request):
        user = UserSerializer(data=request.data)
        if user.is_valid(raise_exception=True):
            user.save()
        return Response(status=201)

    def put(self, request, pk):
        try:
            instance = User.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = UserSerializer(data=request.data, instance=instance)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"user": serializer.data})

    def delete(self, request, pk):
        try:
            User.objects.filter(pk=pk).delete()
        except:
            return Response({"error": "Object does not exists"})
        return Response(status=200)


class MagazineListAPIView(ListAPIView):
    queryset = Magazine.objects.all()
    serializer_class = MagazineSerializer


class MagazineAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == "PUT" or self.request.method == "DELETE":
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request, pk):
        magazine = Magazine.objects.get(pk=pk)
        serializer = MagazineSerializer(magazine)
        return Response(data=serializer.data)

    def post(self, request):
        magazine = MagazineSerializer(data=request.data)
        if magazine.is_valid(raise_exception=True):
            magazine.save()
        return Response(status=201)

    def put(self, request, pk):
        try:
            instance = Magazine.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})
        serializer = MagazineSerializer(data=request.data, instance=instance)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"magazine": serializer.data})

    def delete(self, request, pk):
        try:
            Magazine.objects.filter(pk=pk).delete()
        except:
            return Response({"error": "Object does not exists"})
        return Response(status=200)


class SubscriptionListAPIView(ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class SubscriptionAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == "GET":
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]


    def get(self, request, pk):
        subscription = Subscription.objects.get(pk=pk)
        serializer = SubscriptionSerializer(subscription)
        return Response(data=serializer.data)

    def post(self, request):
        serializer = EditionChoiceSerializer(data=request.data)
        if serializer.is_valid():
            magazine_id = serializer.validated_data['magazine']
            time_amount = serializer.validated_data['time_amount']
            user = request.user
            if not Subscription.objects.filter(subscriber=user, magazine=magazine_id).exists():
                try:
                    magazine = get_object_or_404(Magazine, id=magazine_id)
                except Http404:
                    return Response({'error': 'Magazine not found.'}, status=status.HTTP_404_NOT_FOUND)
                subscription = Subscription.create_subscription(magazine, time_amount, user)
                subscription.save()
            else:
                subscription = Subscription.objects.filter(subscriber=user, magazine=magazine_id).first()
                subscription.increase_end_date(time_amount)
                subscription.save()
            payment = Payment.create_payment(subscription, time_amount)
            payment.save()
        return Response(status=201)

    def delete(self, request, pk):
        try:
            Subscription.objects.filter(pk=pk).delete()
        except:
            return Response({"error": "Object does not exists"})
        return Response(status=200)


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentAPIView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
    def get(self, request, pk):
        payment = Payment.objects.get(pk=pk)
        serializer = PaymentSerializer(payment)
        return Response(data=serializer.data)
