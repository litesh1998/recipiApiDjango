from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from core.models import Tag, Ingrediant, Recipe

from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        '''return Attribute for current user only'''
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        '''Create a new Attribute'''
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngrediantViewSet(BaseRecipeAttrViewSet):
    queryset = Ingrediant.objects.all()
    serializer_class = serializers.IngrediantSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')