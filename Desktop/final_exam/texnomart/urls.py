from django.contrib import admin
from django.urls import path,include
from texnomart import views
from rest_framework.routers import DefaultRouter
#from .views import ProductViewSet


app_name = 'texnomart'

#router = DefaultRouter()
#router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', views.AllProductList.as_view(), name='all_products'),
    path('categories/',views.CategoryListView.as_view(), name='category_list'),
    path('category/add-category/',views.CategoryListCreateView.as_view(),name='add_category'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
     
    # Products
    path('product/add/',views.ProductListCreateView.as_view(), name='add_product'),
    path('product/detail/<int:id>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:id>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:id>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    #c*router.urls,
    
    #Login and Register
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('register/',views.RegisterUserAPI.as_view(), name='register'),
    
    # Product Attributes
    path('product/<int:product_id>/product-attributes/', views.ProductAttributeListViewByProduct.as_view(), name='product_attribute_list_by_product'),
    path('attribute-key/',views.AttributeKeysList.as_view(),name='attribute_key_list'),
    path('attribute-value/',views.AttributeValuesList.as_view(), name='attribute_value_list')
]
