from django.contrib.postgres.aggregates import ArrayAgg
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.api.v1.services.filters_person import filter_role_person
from movies.models import Filmwork, PersonFilmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        return self.model.objects.all().values(
            "id",
            "title",
            "description",
            "creation_date",
            "rating",
            "type",
        ).annotate(genres=ArrayAgg('genres__name', distinct=True),
                   actors=filter_role_person(
                       role=PersonFilmwork.Role.ACTOR),
                   directors=filter_role_person(
                       role=PersonFilmwork.Role.DIRECTOR),
                   writers=filter_role_person(
                       role=PersonFilmwork.Role.WRITER))

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        title = self.request.GET.get("title")

        if title:
            queryset = queryset.filter(title__icontains=title)

        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, self.paginate_by)
        context = {
            'count': paginator.count,
            'prev': (
                page.previous_page_number() if page.has_previous() else None),
            'next': page.next_page_number() if page.has_next() else None,
            'total_pages': paginator.num_pages,
            'results': list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return self.get_object()
