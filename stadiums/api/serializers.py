from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from stadiums.models import Match, Seat, Stadium
from transactions.models import PurchaseMatch


class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = ['id', 'name', 'address', 'phone_number', ]


class MatchSerializer(serializers.ModelSerializer):
    stadium = StadiumSerializer(read_only=True)
    seat_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Match
        fields = ['id', 'title', 'seat_id', 'stadium', 'execute_time_range', ]
        read_only_fields = ['id', 'title', 'execute_time_range', ]

    def create(self, validated_data):
        seat_id = validated_data['seat_id']
        match = validated_data['match']
        seat = get_object_or_404(Seat, **{'id': seat_id, 'stadium': match.stadium})

        with transaction.atomic():
            if PurchaseMatch.objects.filter(seat=seat, match=match, is_paid=True).exists():
                raise serializers.ValidationError(_("This seat has already been taken!"))
            PurchaseMatch.objects.create(
                seat=seat,
                match=match,
                is_paid=True,
                user=validated_data['user'],
                price=max(seat.price - seat.price_discount, 0)
            )
        return match
