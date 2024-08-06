from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        

# For Category
class Category(BaseModel):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name_plural = 'Categories'

# For products        
class Product(BaseModel):
    product_name = models.CharField(max_length=255, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    discount = models.IntegerField(default=0)
    users_like = models.ManyToManyField(User,related_name='likes', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    
    # For discount
    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)

        return self.price
    
    # Pay monthly
    @property
    def pay_monthly_6(self):
        return self.price / 6
    
    @property
    def pay_monthly_12(self):
        return self.price / 12
    
    @property
    def pay_monthly_24(self):
        return self.price / 24
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name
    
class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_images', null=True, blank=True)
    
    is_primary = models.BooleanField(default=False)
    

#For comments   
class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        ZERO = 0
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
    negative_message = models.TextField()
    positive_message = models.TextField()
    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.ZERO.value, null=True, blank=True)
    file = models.FileField(upload_to='comments/', null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name = 'comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    

#For attributes
class Attribute(models.Model):
    attribute_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.attribute_name
    
class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=100)
    
    def __str__(self):
        return self.attribute_value

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    key = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    
    
    
    
    
