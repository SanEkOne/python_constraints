from django.contrib import admin
from .models import Author, Book, Publishment, Country

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Publishment)
admin.site.register(Country)
