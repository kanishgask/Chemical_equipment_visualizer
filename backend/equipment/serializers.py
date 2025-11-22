from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dataset, Equipment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']


class DatasetSerializer(serializers.ModelSerializer):
    equipment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'filename', 'uploaded_at', 'total_records',
            'avg_flowrate', 'avg_pressure', 'avg_temperature',
            'equipment_count'
        ]
    
    def get_equipment_count(self, obj):
        return obj.equipment.count()


class DatasetDetailSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(many=True, read_only=True)
    type_distribution = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'filename', 'uploaded_at', 'total_records',
            'avg_flowrate', 'avg_pressure', 'avg_temperature',
            'equipment', 'type_distribution'
        ]
    
    def get_type_distribution(self, obj):
        from django.db.models import Count
        distribution = obj.equipment.values('equipment_type').annotate(
            count=Count('id')
        ).order_by('-count')
        return {item['equipment_type']: item['count'] for item in distribution}