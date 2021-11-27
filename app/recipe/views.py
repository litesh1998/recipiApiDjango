from core.models import Ingrediant, Recipe, Tag
from rest_framework import mixins, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        '''return Attribute for current user only'''
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)
        return queryset.filter(
            user=self.request.user
            ).order_by('-name').distinct()

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

    def _params_to_int(self, qs: str):
        '''Convert a list of string ids to a list of integers'''
        return list(map(int, qs.split(',')))

    def get_queryset(self):
        tags = self.request.query_params.get('tags')
        ingrediants = self.request.query_params.get('ingrediants')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_int(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingrediants:
            ing_ids = self._params_to_int(ingrediants)
            queryset = queryset.filter(ingrediants__id__in=ing_ids)
        return queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        '''Return Appropirate serializer Class'''
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        '''Create a new Recipe'''
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        '''Upload Image to Recipe'''
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
