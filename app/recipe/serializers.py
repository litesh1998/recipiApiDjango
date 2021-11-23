from rest_framework import serializers
from core.models import Tag, Ingrediant, Recipe


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


class RecipeSerializer(serializers.ModelSerializer):
    '''Recipe Serializer'''
    ingrediants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingrediant.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingrediants', 'tags', 'time_minutes',
                  'price', 'link')
        read_only_fields = ('id',)
