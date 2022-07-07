from django.shortcuts import render, HttpResponse
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from .serializer import FlightSerializer
from .models import Flight


class InternalServerError(APIException):
    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)
        self.default_detail = detail
        self.status_code = code




@api_view(['GET'])
def getFlights(request):
    flights = Flight.objects.all()
    serializedFlightsInfo = FlightSerializer(flights, many=True)
    return Response(serializedFlightsInfo.data)

@api_view(['POST'])
def flightList(request):

    if "arrival_city" not in request.data:
        raise InternalServerError("Please set the arrival city", 500)
        return None
    
    if "departure_city" not in request.data:
        raise InternalServerError("Please set the departure city", 500)
        return None

    query = f''' SELECT f1.id, f2.id FROM flight_flight f1, flight_flight f2 
                WHERE f1.arrival_city = f2.departure_city AND f2.arrival_city = "{request.data['arrival_city']}" AND f1.departure_city = "{request.data['departure_city']}" 
                ORDER BY f1.departure_time, f2.arrival_time
                '''
    cursor = connection.cursor()
    cursor.execute(query)
    row = cursor.fetchone()

    if(row != None):
        flights = Flight.objects.filter(id__in=row)
    elif(row==None):
        flights = Flight.objects.filter(arrival_city=request.data['arrival_city']).filter(departure_city=request.data['departure_city'])
    
    if(flights != None):
        serializedFlightsInfo = FlightSerializer(flights, many=True)
        return Response(serializedFlightsInfo.data)

    return Response("No Flights Found")

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