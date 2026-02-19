from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models

# Dummy models for demo (replace with real models)
class Assessment(models.Model):
    id = models.AutoField(primary_key=True)
    vendor_id = models.IntegerField(default=1)
    vendor_name = models.CharField(max_length=255, default="Vendor")
    status = models.CharField(max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'common'

class Vendor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default="Vendor")
    category = models.CharField(max_length=100, default="General")
    status = models.CharField(max_length=50, default="Active")
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'common'


# Serializers
from rest_framework import serializers

class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ['id', 'vendor_id', 'vendor_name', 'status', 'created_at']

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'category', 'status', 'email', 'phone', 'created_at']


# ViewSets
class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    permission_classes = [IsAuthenticated]

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]
