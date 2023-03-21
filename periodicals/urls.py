from django.urls import path, include

from periodicals.views import *

urlpatterns = [path("users/", UserListAPIView.as_view()),
               path("create-user/", UserAPIView.as_view()),
               path("user/<int:pk>", UserAPIView.as_view()),

               path("magazines/", MagazineListAPIView.as_view()),
               path("create-magazine/", MagazineAPIView.as_view()),
               path("magazine/<int:pk>", MagazineAPIView.as_view()),

               path("subscriptions/", SubscriptionListAPIView.as_view()),
               path("create-subscription/", SubscriptionAPIView.as_view()),
               path("subscription/<int:pk>", SubscriptionAPIView.as_view()),

               path("payments/", PaymentListAPIView.as_view()),
               path("payment/<int:pk>", PaymentAPIView.as_view()),

               path("authorization/",include("rest_framework.urls")),
               ]
