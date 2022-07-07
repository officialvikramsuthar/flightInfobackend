from rest_framework import serializers
from .models import Flight
import time


class JsTimestampField(serializers.Field):
    def to_representation(self, value):
        return int(time.mktime(value.timetuple()))

class FlightSerializer(serializers.ModelSerializer):
    #departure_time = JsTimestampField(source="departure_time")
    # arrival_time = JsTimestampField(source="arrival_time")
    class Meta:
        model = Flight
        fields = '__all__'
    
    def to_representation(self, instance):
        f_departure_time = int(time.mktime(instance.departure_time.timetuple())) 
        f_arrival_time = int(time.mktime(instance.arrival_time.timetuple()))

        return {'id': instance.id,
                'ticket_number': instance.ticket_number,
                'departure_city':instance.departure_city,
                'arrival_city':instance.arrival_city,
                'departure_time': f_departure_time,
                'arrival_time': f_arrival_time}
