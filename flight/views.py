from django.shortcuts import render, HttpResponse
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .serializer import FlightSerializer
from .models import Flight

@api_view(['GET'])
def apiOverview(request):
    return Response("Hello")

@api_view(['POST'])
def flightList(request):
    
    cursor = connection.cursor()
    print(request.data['departure_city'])
    query = f''' SELECT * FROM flight_flight f1, flight_flight f2 
                WHERE f1.arrival_city = f2.departure_city AND f2.arrival_city = "request.data['arrival_city']" AND f1.departure_city = "request.data['departure_city']" 
                ORDER BY f1.departure_time, f2.arrival_time
                '''
    cursor.execute(query)
    row = cursor.fetchone()
    flights = Flight.objects.filter(id__in=row)
    print(flights)
    serializedFlightsInfo = FlightSerializer(flights, many=True)


    return Response(serializedFlightsInfo.data)

@api_view(['POST'])
def createFlight(request):
    serializer = FlightSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def updateFlight(request, pk):
    flight = Flight.objects.get(id=pk)
    serializer = FlightSerializer(instance=flight, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)