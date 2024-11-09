from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q


def filter_role_person(role):
    return ArrayAgg('persons__full_name',
                    filter=Q(person_filmwork__role=role),
                    distinct=True)
