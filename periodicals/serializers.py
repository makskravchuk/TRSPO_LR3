from rest_framework import serializers

from periodicals.models import User, Magazine, Subscription, Payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class MagazineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Magazine
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class EditionChoiceSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    magazine = serializers.IntegerField()
    time_amount = serializers.IntegerField(min_value=1)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
