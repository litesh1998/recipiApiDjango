from rest_framework import serializers
from core.models import Tag, Ingrediant


class TagSerializer(serializers.ModelSerializer):
    '''Serializer for tag objects'''

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngrediantSerializer(serializers.ModelSerializer):
    '''Serializer for Ingrediant Model'''

    class Meta:
        model = Ingrediant
        fields = ('id', 'name')
        read_only_fields = ('id',)
