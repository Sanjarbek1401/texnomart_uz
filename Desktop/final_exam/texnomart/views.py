from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth.models import User
from knox.models import AuthToken
from texnomart.serializers import *
#from .serializers import CategoryModelSerializer, ProductSerializer, UserModelSerializer,CategoryListSerializer,AllProductsModelSerializer,ProductAttributeModelSerializer,ProductAttributeFilterSerializer
from .models import Category, Product,ProductAttribute,Attribute
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Category List View
class CategoryListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    model = Category
    serializer_class = CategoryListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['category_name', ]
    search_fields = ['category_name', ]
    ordering_fields = ['category_name', ]

    def get_queryset(self):
        queryset = Category.objects.prefetch_related('products').all()
        return queryset

    @method_decorator(cache_page(30))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
#add category   
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [permissions.AllowAny]

    @method_decorator(cache_page(60*15))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

#detail category
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'



#Getting All Products
class AllProductList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    model = Product
    serializer_class = AllProductsModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['product_name', 'price']
    search_fields = ['product_name', 'price']
    ordering_fields = ['product_name', 'price']

    def get_queryset(self):
        queryset = Product.objects.prefetch_related(
                                                    'users_like',
                                                    'users_like__comment_set').all()
        return queryset

    @method_decorator(cache_page(30))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

  


# Product ModelViewSet
""" class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('category').prefetch_related('users_like', 'comments')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['price','category' ]
    search_fields = ['product_name','price']

    @method_decorator(cache_page(60*15))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return Product.objects.all().select_related('category').prefetch_related('users_like', 'comments')

    def get_serializer_context(self):
        return {'request': self.request} """
        
#detail product       
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all().select_related('category').prefetch_related('users_like', 'comments')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

    @method_decorator(cache_page(60*15))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_serializer_context(self):
        return {'request': self.request}
    
#Add product      
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all().select_related('category').prefetch_related('users_like', 'comments')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    @method_decorator(cache_page(60*15))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_serializer_context(self):
        return {'request': self.request}

#Update product
class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all().select_related('category').prefetch_related('users_like', 'comments')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

    def get_serializer_context(self):
        return {'request': self.request}
    
#delete product
class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all().select_related('category').prefetch_related('users_like', 'comments')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'







# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

# Register User API
class RegisterUserAPI(generics.GenericAPIView):
    serializer_class = UserModelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=serializer.data['username'])
            token_obj, _ = Token.objects.get_or_create(user=user)
            return Response({'status': 200, 'payload': serializer.data, 'token': str(token_obj)})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# For product Attributes
class ProductAttributeListViewByProduct(generics.ListAPIView):
    serializer_class = ProductAttributeModelSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['key__attribute_name', 'value__attribute_value']
    ordering_fields = ['key', 'value']

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductAttribute.objects.filter(product_id=product_id).select_related('key', 'value', 'product')
    
    
    
class AttributeKeysList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    model = Attribute
    serializer_class = AttributeModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['attribute_name', ]
    search_fields = ['attribute_name', ]
    ordering_fields = ['attribute_name', ]
    queryset = Attribute.objects.all()

    @method_decorator(cache_page(30))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class AttributeValuesList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    model = AttributeValue
    serializer_class = AttributeValueModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['attribute_value', ]
    search_fields = ['attribute_value', ]
    ordering_fields = ['attribute_value', ]
    queryset = AttributeValue.objects.all()

    @method_decorator(cache_page(30))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)