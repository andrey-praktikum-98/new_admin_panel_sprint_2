from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .services.abstract_models import (TimeStampedCreatedMixin,
                                       TimeStampedMixin, UUIDMixin)


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        indexes = [
            models.Index(fields=['full_name'], name='person_full_name_idx'),
        ]

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):
    class MediaType(models.TextChoices):
        MOVIE = 'movie', 'Movie'
        TV_SHOW = 'tv_show', 'TV Show'

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation_date'), blank=True)
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    type = models.CharField(
        max_length=10,
        choices=MediaType.choices,
        default=MediaType.MOVIE,
    )
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('filmfork')
        verbose_name_plural = _('filmforks')
        indexes = [
            models.Index(fields=['id'], name='film_work_id_idx'),
            models.Index(fields=['title'], name='film_work_title_idx'),
            models.Index(fields=['creation_date'],
                         name='film_work_creation_date_idx'),
            models.Index(fields=['rating'], name='film_work_creation_idx'),
            models.Index(fields=['type'], name='film_work_type_idx'),
        ]

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin, TimeStampedCreatedMixin):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE,
                                  verbose_name=_('filmwork'),
                                  related_name="genre_filmwork")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,
                              verbose_name=_('genre'),
                              related_name="genre_filmwork")

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('genre filmwork')
        verbose_name_plural = _('genres filmworks')
        indexes = [
            models.Index(fields=['film_work', 'genre'],
                         name='genre_film_work_idx_fk'),
        ]
        unique_together = ["film_work", "genre"]


class PersonFilmwork(UUIDMixin, TimeStampedCreatedMixin):
    class Role(models.TextChoices):
        DIRECTOR = 'director', 'Director'
        WRITER = 'writer', 'Writer'
        ACTOR = 'actor', 'Actor'

    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE,
                                  verbose_name=_('filmwork'),
                                  related_name="person_filmwork")
    person = models.ForeignKey(Person, on_delete=models.CASCADE,
                               verbose_name=_('person'),
                               related_name="person_filmwork")
    role = models.CharField(
        _('role'),
        max_length=10,
        choices=Role.choices,
        default=Role.ACTOR,
    )

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('person filmwork')
        verbose_name_plural = _('persons filmworks')
        indexes = [
            models.Index(fields=['film_work', 'person', 'role'],
                         name='person_role_film_work_idx_fk'),
        ]
        unique_together = ["film_work", "person", "role"]
