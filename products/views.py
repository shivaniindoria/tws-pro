from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta

from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
 

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.retrieved_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False)
    def top_5_all(self, request):
        top_products = Product.objects.order_by('-retrieved_count')[:5]
        serializer = self.get_serializer(top_products, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def top_5_last_day(self, request):
        since = timezone.now() - timedelta(days=1)
        top_products = Product.objects.filter(retrieved_count__gt=0, updated_at__gte=since).order_by('-retrieved_count')[:5]
        serializer = self.get_serializer(top_products, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def top_5_last_week(self, request):
        since = timezone.now() - timedelta(weeks=1)
        top_products = Product.objects.filter(retrieved_count__gt=0, updated_at__gte=since).order_by('-retrieved_count')[:5]
        serializer = self.get_serializer(top_products, many=True)
        return Response(serializer.data)

