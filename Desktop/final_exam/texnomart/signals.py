import json
import os
from django.db.models.signals import post_save,pre_save,post_delete,pre_delete
from django.core.mail import send_mail
from config.settings import BASE_DIR
from config.settings import DEFAULT_FROM_EMAIL
from texnomart.models import Category,Product
from django.dispatch import receiver


# to create signals with decorators for CATEGORY
@receiver(post_save, sender= Category)
def post_save_category(sender, instance, created, **kwargs):
    if created:
        print('Category was created')
        subject = 'Category was created'
        message = f'{instance.category_name} was created by admin'
        from_email = DEFAULT_FROM_EMAIL
        to = 'sanjarbahodirov9901@gmail.com'
        send_mail(subject,message,from_email,[to,],fail_silently=False)
    else:
        print('Category was updated')
        
        
@receiver(pre_save,sender=Category)
def pre_save_category(sender, instance, **kwargs):
    print('After save category')
    

@receiver(pre_delete,sender = Category)
def pre_delete_category(sender, instance,**kwargs):
    file_path = os.path.join(BASE_DIR,'texnomart/deleted_category', f'category.{instance.id}.json')
    
    category_data = {
        'id': instance.id,
        'category_name': instance.category_name,
        'slug':instance.slug
    }
    with open(file_path,'w') as json_file:
            json.dump(category_data,json_file,indent=4)
    print('Category was saved before deleted')
    
# to create signals with decorators for PRODUCTS    
@receiver(post_save, sender= Product)
def post_save_product(sender, instance, created, **kwargs):
    if created:
        print('Product was created')
        subject = 'Product was created'
        message = f'{instance.product_name} was created by admin'
        from_email = DEFAULT_FROM_EMAIL
        to = 'sanjarbahodirov9901@gmail.com'
        send_mail(subject,message,from_email,[to,],fail_silently=False)
    else:
        print('Product was updated')
  
#delete product        
@receiver(pre_delete,sender = Product)
def pre_delete_product(sender, instance,**kwargs):
    file_path = os.path.join(BASE_DIR,'texnomart/deleted_products', f'product.{instance.id}.json')
    
    product_data = {
        'id': instance.id,
        'product_name': instance.product_name,
        'description':instance.description,
        'price':instance.price,
        'discount':instance.discount,      
        'slug':instance.slug
    }
    with open(file_path,'w') as json_file:
            json.dump(product_data,json_file,indent=4)
    print('product was saved before deleted')
    