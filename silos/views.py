from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Silo, SiloLog
from .serializers import SiloSerializer, SiloLogSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class SiloListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'manager':
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        silos = Silo.objects.all()
        serializer = SiloSerializer(silos, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != 'manager':
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        serializer = SiloSerializer(data=request.data)
        if serializer.is_valid():
            silo = serializer.save()
            return Response(SiloSerializer(silo).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SiloLogView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, silo_id):
        if request.user.role != 'manager':
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        silo = get_object_or_404(Silo, id=silo_id)

        serializer = SiloLogSerializer(data=request.data, context={'silo': silo})
        if serializer.is_valid():
            log = serializer.save()

            if log.change_type == 'incoming':
                silo.current_stock += log.amount
            elif log.change_type == 'outgoing':
                if silo.current_stock < log.amount:
                    return Response({"detail": "Not enough stock available."}, status=status.HTTP_400_BAD_REQUEST)
                silo.current_stock -= log.amount
            silo.save()

            return Response(SiloLogSerializer(log).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)