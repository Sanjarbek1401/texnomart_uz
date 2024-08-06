from rest_framework import serializers
from .models import Image,Category,Comment,ProductAttribute,Product,AttributeValue,Attribute
from django.contrib.auth.models import User
from django.db.models.functions import Round
from django.db.models import Avg

# For Image
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'is_primary','product','category']
 
 
 
        
#For Comments
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ()
        
 
        
#For Products
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source = 'product.category.category_name', read_only = True)
    category_slug  = serializers.SlugField(source = 'product.category.slug',read_only =True)
    primary_images = serializers.SerializerMethodField()
    all_images = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True,read_only = True)
    comments_count = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
       
    # Get attributes
    def get_attributes(self,instance):
        attributes = ProductAttribute.objects.filter(product = instance).values_list('key_id','key__attribute_name',
                                                                                     'value_id','value__attribute_value')
        characters = [
            {
            'attribute_id':key_id,
            'attribute_name':key_name,
            'attribute_value_id':value_id,
            'attribute_value':value_name
            }
            for key_id,key_name,value_id,value_name in attributes
        ]
        return characters
    
    #Get avarage rating
    def get_avg_rating(self,instance):
        avg_rating = Comment.objects.filter(product=instance).aggregate(avg_rating=Round(Avg('rating')))
        if avg_rating.get('avg_rating'):
            return avg_rating.get('avg_rating')
        return 0
    
    #Get comments count
    def get_comments_count(self,instance):
        count = Comment.objects.filter().count()
        return count 
    
    #Get users like
    def get_is_liked(self,instance):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        all_likes = instance.users_like.all()
        if user in all_likes:
            return True
        return False
    
    # Get all images
    def get_all_images(self,instance):
        images = Image.objects.all().filter(product=instance)
        all_images = []
        request = self.context.get('request')
        for image in images:
            all_images.append(request.build_absolute_uri(image.image.url))
        return all_images
    
    #Get primary image
    def get_primary_images(self,instance):
        image = Image.objects.filter(product=instance, is_primary = True).first()
        request = self.context.get('request')
        if image:
            image_url = image.image.url
            return request.build_absolute_uri(image_url)
     
    class Meta:
        model = Product
        exclude = ('users_like',)
        extra_fields = ['category_name','category_slug','primary_images','all_images','is_liked']






# For Category
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude  =() 
        
class CategoryModelSerializer(serializers.ModelSerializer):
    category_image = serializers.SerializerMethodField(method_name='get_images')
    products = ProductSerializer(many=True,read_only = True)
    
    def get_images(self, instance):
        image = Image.objects.filter(category=instance, is_primary=True).first()
        request = self.context.get('request')
        if image:
            image_url = image.image.url
            return request.build_absolute_uri(image_url)     
        return None

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'slug', 'category_image','products']
        
#For getting all products wit categories
class AllProductsModelSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()

    def get_avg_rating(self, instance):
        avg_rating = instance.comments.aggregate(avg_rating=Round(Avg('rating')))
        if avg_rating.get('avg_rating'):
            return avg_rating.get('avg_rating')
        return 0

    def get_is_liked(self, instance):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        all_likes = instance.users_like.all()
        if user in all_likes:
            return True
        return False

    # Get primary image
    def get_primary_image(self, instance):
        image = instance.product_images.filter(is_primary=True).first()
        request = self.context.get('request')
        if image:
            image_url = image.image.url
            return request.build_absolute_uri(image_url)

    class Meta:
        model = Product
        exclude = ('category', 'users_like', 'description')
    
    
    
    
           
# For login, register,logout
from rest_framework import serializers
from django.contrib.auth.models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'])
        # user = User.objects.create_superuser(validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user



# For product Attributes
class AttributeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        exclude = ()

class AttributeValueModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        exclude = ()


class ProductAttributeModelSerializer(serializers.ModelSerializer):
    key = serializers.StringRelatedField()
    value = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    
    class Meta:
        model = ProductAttribute
        fields = ('key', 'value', 'product',)

class ProductAttributeFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ('key', 'value', 'product',)
        


