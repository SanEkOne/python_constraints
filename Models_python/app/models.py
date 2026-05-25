from django.db import models
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    name = models.CharField(_("Ім'я"), max_length=255)
    birth_year = models.IntegerField(_("Рік народження"), null=True, blank=True)
    rating = models.FloatField(_("Рейтинг"), default=0.0)
    country = models.ForeignKey(
        "Country", on_delete=models.CASCADE, related_name="authors", verbose_name=_("Країна"),
        null=True,     
        blank=True
    )

    class Meta:
        verbose_name = _("Автор")
        verbose_name_plural = _("Автори")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["rating"]),
        ]

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(_("Назва"), max_length=255)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="books", verbose_name=_("Автор")
    )
    pages = models.IntegerField(_("Кількість сторінок"), null=True, blank=True)
    price = models.DecimalField(_("Ціна"), max_digits=8, decimal_places=2)
    published_year = models.IntegerField(_("Рік видання"), null=True, blank=True)
    stock = models.IntegerField(_("Залишок на складі"), default=0)
    publishment = models.ForeignKey(
        "Publishment",
        on_delete=models.CASCADE,
        related_name="books",
        verbose_name=_("Видавництво"),
        null=True, blank=True
    )


    class Meta:
        verbose_name = _("Книга")
        verbose_name_plural = _("Книги")
        ordering = ["-published_year", "title"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["published_year"]),
            models.Index(fields=["price"]),
        ]

    def __str__(self):
        return self.title


class Publishment(models.Model):
    name = models.CharField(_("Назва видавництва"), max_length=255)
    country = models.ForeignKey(
        "Country", on_delete=models.CASCADE, related_name="publishments", verbose_name=_("Країна"),
        null=True, blank=True
    )

    class Meta:
        verbose_name = _("Видавництво")
        verbose_name_plural = _("Видавництва")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(_("Назва країни"), max_length=255)

    class Meta:
        verbose_name = _("Країна")
        verbose_name_plural = _("Країни")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name
