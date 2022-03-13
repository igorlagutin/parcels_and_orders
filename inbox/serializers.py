from rest_framework import serializers


class SerialDeliverSerializer(serializers.Serializer):
    serial = serializers.IntegerField()
    deliver_name = serializers.CharField()
