from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .models import Manufacturer, Category , Product
from django.utils.text import slugify



def home(request):
    message = None

    if request.method == 'POST' and request.POST.get('action') == 'create':
        name = request.POST.get('name', '').strip()
        price = request.POST.get('price', '').strip()
        description = request.POST.get('description', '').strip()
        short_description = request.POST.get('short_description', '').strip()
        category = request.POST.get('category', '').strip() # передать объект категории
        manufacturer = request.POST.get('manufacturer', '').strip()

        if name:
            Product.objects.create(
                name=name,
                price=float(price) if price else None,
                description=description,
                short_description=short_description,
                category=Category.objects.get(id=category) if category else None,
                manufacturer=Manufacturer.objects.get(id=manufacturer) if manufacturer else None,
            )
            message = f'Продукт "{name}" додано!'
        else:
            message = 'Помилка: введіть назву продукту.'

    elif request.method == 'POST' and request.POST.get('action') == 'update':
        product_id = request.POST.get('product_id')
        name = request.POST.get('name', '').strip()
        price = request.POST.get('price', '').strip()
        description = request.POST.get('description', '').strip()
        short_description = request.POST.get('short_description', '').strip()
        category = request.POST.get('category', '').strip()
        manufacturer = request.POST.get('manufacturer', '').strip()

        try:
            product = Product.objects.get(id=product_id)
            product.name = name
            product.price = float(price) if price else None
            product.description = description
            product.short_description = short_description
            product.category = category
            product.manufacturer = Manufacturer.objects.get(id=manufacturer) if manufacturer else None
            product.save()
            message = f'Продукт "{product.name}" оновлено!'
        except (Product.DoesNotExist, Manufacturer.DoesNotExist):
            message = 'Продукт або виробник не знайдено.'


    elif request.method == 'POST' and request.POST.get('action') == 'delete':
        product_id = request.POST.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
            name = product.name
            product.delete()
            message = f'Продукт "{name}" видалено.'
        except Product.DoesNotExist:
            message = 'Продукт не знайдено.'

    categories_list = Category.objects.all().order_by('name')
    manufacturers_list = Manufacturer.objects.all().order_by('name')
    products = Product.objects.all().order_by('id')

    return render(request, 'app/index.html', {
        'title': 'Продукти',
        'year': datetime.now().year,
        'categories_list': categories_list,    
        'manufacturers_list': manufacturers_list,
        'products': products,
        'message': message,
    })

###################################################################
def category(request):
    message = None

    if request.method == 'POST' and request.POST.get('action') == 'create':
        name = request.POST.get('name', '').strip()
        if name:
            Category.objects.create(name=name)
            message = f'Категорію "{name}" додано!'
        else:
            message = 'Помилка: введіть назву категорії.'

    elif request.method == 'POST' and request.POST.get('action') == 'update':
        category_id = request.POST.get('category_id')
        name = request.POST.get('name', '').strip()
        try:
            category = Category.objects.get(id=category_id)
            category.name = name
            category.save()
            message = f'Категорію "{name}" оновлено!'
        except Category.DoesNotExist:
            message = 'Категорію не знайдено.'

    elif request.method == 'POST' and request.POST.get('action') == 'delete':
        category_id = request.POST.get('category_id')
        try:
            category = Category.objects.get(id=category_id)
            name = category.name
            category.delete()
            message = f'Категорію "{name}" видалено.'
        except Category.DoesNotExist:
            message = 'Категорію не знайдено.'

    categories = Category.objects.all().order_by('id')

    return render(request, 'app/category.html', {
        'title': 'Category',
        'message': message,
        'categories': categories,
        'year': datetime.now().year,
    })


def manufacturer(request):
    message = None

    if request.method == 'POST' and request.POST.get('action') == 'create':
        name = request.POST.get('name', '').strip()
        country = request.POST.get('country', '').strip()
        website = request.POST.get('website', '').strip()
        email = request.POST.get('email', '').strip()
        established_year = request.POST.get('established_year', '').strip()

        if name and country:
            try:
                Manufacturer.objects.create(
                    name=name,
                    country=country,
                    website=website if website else None,
                    email=email if email else None,
                    established_year=int(established_year) if established_year else None
                )
                message = f'Виробника "{name}" додано!'
            except Exception as e:
                message = f'Помилка при додаванні: {e}'
        else:
            message = 'Помилка: назва та країна є обовʼязковими полями.'

    elif request.method == 'POST' and request.POST.get('action') == 'update':
        manufacturer_id = request.POST.get('manufacturer_id')
        name = request.POST.get('name', '').strip()
        country = request.POST.get('country', '').strip()
        website = request.POST.get('website', '').strip()
        email = request.POST.get('email', '').strip()
        established_year = request.POST.get('established_year', '').strip()

        try:
            manufacturer_obj = Manufacturer.objects.get(id=manufacturer_id)
            if name and country:
                manufacturer_obj.name = name
                manufacturer_obj.country = country
                manufacturer_obj.website = website if website else None
                manufacturer_obj.email = email if email else None
                manufacturer_obj.established_year = int(established_year) if established_year else None
                manufacturer_obj.save()
                message = f'Дані виробника "{name}" оновлено!'
            else:
                message = 'Помилка: назва та країна не можуть бути порожніми.'
        except Manufacturer.DoesNotExist:
            message = 'Виробника не знайдено.'
        except Exception as e:
            message = f'Помилка при оновленні: {e}'

    elif request.method == 'POST' and request.POST.get('action') == 'delete':
        manufacturer_id = request.POST.get('manufacturer_id')
        try:
            manufacturer_obj = Manufacturer.objects.get(id=manufacturer_id)
            name = manufacturer_obj.name
            manufacturer_obj.delete()
            message = f'Виробника "{name}" видалено.'
        except Manufacturer.DoesNotExist:
            message = 'Виробника не знайдено.'

    # Отримуємо всіх виробників для виведення в таблицю
    manufacturers = Manufacturer.objects.all().order_by('id')

    return render(request, 'app/manufacturer.html', {
        'title': 'Виробники',
        'message': message,
        'manufacturers': manufacturers,
        'year': datetime.now().year,
    })