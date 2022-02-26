from django.shortcuts import render
from django.http import Http404
# from rest_auth.registration.views import RegisterView
from dj_rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from users.permissions import IsOwnerOrReadOnly
from .models import Instructor, Other
from .serializers import (
    InstructorRegistrationSerializer, 
    OtherRegistrationSerializer , 
    InstructorSerializer,
    OtherSerializer,
    )




# --- Instructor --- #

class InstructorRegistrationView(RegisterView):
    serializer_class = InstructorRegistrationSerializer

class InstructorAccountView(APIView):
    serializer_class = InstructorSerializer
    queryset = Instructor.objects.all()
    parser_classes = [MultiPartParser]

    def get_object(self, pk):
        try:
            return Instructor.objects.filter(is_active = True).get(id = pk)
        except Instructor.DoesNotExist:
            raise Http404

    def get(self ,request , pk = None , format = None):

        owner = self.get_object(pk)
        serialized_Instructor = InstructorSerializer(owner)
        return Response({ "Instructor-Info" : serialized_Instructor.data, })
    
    def put(self, request, pk, format = None):

        owner = self.get_object(pk)
        serializer = InstructorSerializer(owner, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InstructorAccountDeleteView(APIView):
    serializer_class = InstructorSerializer
    queryset = Instructor.objects.all()
    parser_classes = [MultiPartParser]

    def get_object(self, pk):
        try:
            return Instructor.objects.filter(is_active = True).get(id = pk)
        except Instructor.DoesNotExist:
            raise Http404

    def get(self ,request , pk = None , format = None):

        owner = self.get_object(pk)
        serialized_Instructor = InstructorSerializer(owner)
        return Response({ "Instructor-Info" : serialized_Instructor.data, })
    
    def delete(self, request, pk, format=None):
        owner = self.get_object(pk)
        owner.is_active = False
        owner.save()
        return Response(status=status.HTTP_204_NO_CONTENT)





# --- Other --- #

class OtherRegistrationView(RegisterView):
    serializer_class = OtherRegistrationSerializer

class OtherAccountView(APIView):
    serializer_class = OtherSerializer
    queryset = Other.objects.all()
    parser_classes = [MultiPartParser]

    def get_object(self, pk):
        try:
            return Other.objects.filter(is_active = True).get(id = pk)
        except Other.DoesNotExist:
            raise Http404

    def get(self ,request , pk = None , format = None):

        owner = self.get_object(pk)
        serialized_Other = OtherSerializer(owner)
        return Response({ "Other-Info" : serialized_Other.data, })
    
    def put(self, request, pk, format = None):

        owner = self.get_object(pk)
        serializer = OtherSerializer(owner, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OtherAccountDeleteView(APIView):
    serializer_class = OtherSerializer
    queryset = Other.objects.all()
    parser_classes = [MultiPartParser]

    def get_object(self, pk):
        try:
            return Other.objects.filter(is_active = True).get(id = pk)
        except Other.DoesNotExist:
            raise Http404

    def get(self ,request , pk = None , format = None):

        owner = self.get_object(pk)
        serialized_Other = OtherSerializer(owner)
        return Response({ "Other-Info" : serialized_Instructor.data, })
    
    def delete(self, request, pk, format=None):
        owner = self.get_object(pk)
        owner.is_active = False
        owner.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


