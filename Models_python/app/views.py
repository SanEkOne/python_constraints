from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from app.models import Author


def home(request):
    message = None # повідомлення про успіх/помилку

    # додавання автора
    if request.method == 'POST' and request.POST.get('action') == 'create':
        name       = request.POST.get('name', '').strip()
        birth_year = request.POST.get('birth_year', '').strip()
        rating     = request.POST.get('rating', '').strip()

        if name:
            Author.objects.create( # створюємо нового автора
                name=name,
                birth_year=int(birth_year) if birth_year else None,
                rating=float(rating) if rating else None,
            )
            message = f'Автора "{name}" додано!'
        else:
            message = 'Помилка: введіть ім\'я автора.'

    # оновлення автора
    elif request.method == 'POST' and request.POST.get('action') == 'update':
        author_id  = request.POST.get('author_id')
        name       = request.POST.get('name', '').strip()
        birth_year = request.POST.get('birth_year', '').strip()
        rating     = request.POST.get('rating', '').strip()

        try:
            author            = Author.objects.get(id=author_id)
            author.name       = name
            author.birth_year = int(birth_year) if birth_year else None
            author.rating     = float(rating) if rating else None
            author.save()
            message = f'Автора "{author.name}" оновлено!'
        except Author.DoesNotExist:
            message = 'Автора не знайдено.'

    # видалити автора
    elif request.method == 'POST' and request.POST.get('action') == 'delete':
        author_id = request.POST.get('author_id')
        try:
            author = Author.objects.get(id=author_id)
            name = author.name
            author.delete()
            message = f'Автора "{name}" видалено.'
        except Author.DoesNotExist:
            message = 'Автора не знайдено.'

    # отримання списку всіх авторів для відображення
    authors = Author.objects.all().order_by('id')

    return render(request, 'app/index.html', {
        'title': 'Автори',
        'year': datetime.now().year,
        'authors': authors,
        'message': message,
    })

###################################################################

def contact(request):
    assert isinstance(request, HttpRequest)
    return render(request, 'app/contact.html', {
        'title': 'Contact',
        'message': 'Your contact page.',
        'year': datetime.now().year,
    })


def about(request):
    assert isinstance(request, HttpRequest)
    return render(request, 'app/about.html', {
        'title': 'About',
        'message': 'Your application description page.',
        'year': datetime.now().year,
    })
  