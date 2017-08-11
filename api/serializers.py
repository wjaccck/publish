# encoding: utf8

from django.db.models import Count
from rest_framework import serializers
from netaddr import *
from abstract.serializers import CommonHyperlinkedModelSerializer
from .models import Version_history,Ipv4Address,Ipv4Network


class Version_historyserializers(serializers.HyperlinkedModelSerializer):
    project=serializers.StringRelatedField()
    status=serializers.StringRelatedField()
    class Meta:
        fields = '__all__'
        model = Version_history



class IPv4AddressSerializer(CommonHyperlinkedModelSerializer):

    class Meta:
        fields = '__all__'
        model = Ipv4Address

class IPv4NetworkSerializer(CommonHyperlinkedModelSerializer):


    class Meta:
        fields = '__all__'
        model = Ipv4Network

    def create(self, validated_data):
        prefix = validated_data['name']
        nwk = IPNetwork(prefix)
        rawAddrs = [Ipv4Address(name=str(x), creator=validated_data['creator'], \
                    last_modified_by=validated_data['last_modified_by']) for x in list(nwk)]
        addresses = Ipv4Address.objects.bulk_create(rawAddrs, batch_size=30)
        return super(IPv4NetworkSerializer, self).create(validated_data)

    def validate(self, attrs):
        if attrs['name'].find('/') == -1:
            raise serializers.ValidationError('Network mask is missing!')

        return super(IPv4NetworkSerializer, self).validate(attrs)