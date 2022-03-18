from sqlite3 import Date

import graphene
from graphene.relay import Node
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from .models import DayHistory

# Metric: always 'name' and 'units' + data list


class DayHistoryType(DjangoObjectType):
    # title excerpt
    metrics = GenericScalar()
    workouts = GenericScalar()

    class Meta:
        model = DayHistory
        # fields = ("id", "date", "metrics", "workouts")


class Query(graphene.ObjectType):
    # TODO: resolve metric names
    # TODO: request metric data with 'name' as attribute

    all_dayhistories = graphene.List(DayHistoryType)

    def resolve_all_dayhistories(root, info):
        return (DayHistory.objects.all())


schema = graphene.Schema(query=Query)
