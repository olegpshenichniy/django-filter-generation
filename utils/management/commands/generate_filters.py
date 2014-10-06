# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.core.management import CommandError
from django.db.models import get_model
from django.db.models.fields import (CharField, IntegerField, BigIntegerField,
                                     BooleanField, DateField, DateTimeField,
                                     TextField, TimeField, EmailField,
                                     DecimalField, FloatField, FilePathField,
                                     IPAddressField, PositiveIntegerField,
                                     PositiveSmallIntegerField, SlugField,
                                     SmallIntegerField, URLField)

from django.db.models.fields.related import ForeignKey


TEMPLATE = "\n    {name} = django_filters.{filter_type}Filter(" \
           "name='{attr_name}', " \
           "lookup_type='{lookup_type}')"

CHAR_ICONTAINS = {
    'types': [CharField, TextField, EmailField, FilePathField, IPAddressField,
              SlugField, URLField],
    'lookup_type': 'icontains',
    'filter_type': 'Char'
}
NUMBER_EXACT = {
    'types': [ForeignKey],
    'lookup_type': 'exact',
    'filter_type': 'Number'
}
NUMBER_MAX_MIN = {
    'types': [IntegerField, BigIntegerField, DecimalField, FloatField,
              PositiveIntegerField, PositiveSmallIntegerField, SmallIntegerField],
    'lookup_type': {
        'min': 'gte',
        'max': 'lte'
    },
    'filter_type': 'Number'
}
BOOLEAN_EXACT = {
    'types': [BooleanField],
    'lookup_type': 'exact',
    'filter_type': 'Boolean'
}
TIME_MAX_MIN = {
    'types': [TimeField],
    'lookup_type': {
        'min': 'gte',
        'max': 'lte'
    },
    'filter_type': 'Time'
}
DATE_MAX_MIN = {
    'types': [DateField],
    'lookup_type': {
        'min': 'gte',
        'max': 'lte'
    },
    'filter_type': 'Date'
}
DATE_TIME_MAX_MIN = {
    'types': [DateTimeField],
    'lookup_type': {
        'min': 'gte',
        'max': 'lte'
    },
    'filter_type': 'DateTime'
}


class Command(BaseCommand):
    """
    Fast made command for automation generating django-filters class
    for provided app.Model
    """
    args = '<app app ...>'
    help = 'Generate filters class by provided app.Model'

    def handle(self, *args, **options):
        if not args:
            raise CommandError('Enter app.Model')

        app_name = args[0].split('.')[0]
        model_name = args[0].split('.')[1]

        model = get_model(app_label=app_name, model_name=model_name)

        # add greeting message
        result = "####################################\n" \
                 "\tFILTERS FOR '{0}' MODEL\n" \
                 "####################################" \
                 "\n\n".format(model.__name__)

        # add class name and extend django filters
        result += "class {0}Filter(django_filters.FilterSet):".format(
            model.__name__)

        # loop by modeld fields
        for attr in model._meta.fields[1:]:

            if attr.__class__ in CHAR_ICONTAINS['types']:
                result += TEMPLATE.format(
                    name=attr.name,
                    attr_name=attr.name,
                    filter_type=CHAR_ICONTAINS['filter_type'],
                    lookup_type=CHAR_ICONTAINS['lookup_type']
                )

            elif attr.__class__ in NUMBER_EXACT['types']:
                result += TEMPLATE.format(
                    name=attr.name,
                    attr_name=attr.name,
                    filter_type=NUMBER_EXACT['filter_type'],
                    lookup_type=NUMBER_EXACT['lookup_type'])

            elif attr.__class__ in NUMBER_MAX_MIN['types']:
                result += TEMPLATE.format(
                    name='max_{0}'.format(attr.name),
                    attr_name=attr.name,
                    filter_type=NUMBER_MAX_MIN['filter_type'],
                    lookup_type=NUMBER_MAX_MIN['lookup_type']['max']
                )
                result += TEMPLATE.format(
                    name='min_{0}'.format(attr.name),
                    attr_name=attr.name,
                    filter_type=NUMBER_MAX_MIN['filter_type'],
                    lookup_type=NUMBER_MAX_MIN['lookup_type']['min']
                )

            elif attr.__class__ in BOOLEAN_EXACT['types']:
                result += TEMPLATE.format(
                    name=attr.name,
                    attr_name=attr.name,
                    filter_type=BOOLEAN_EXACT['filter_type'],
                    lookup_type=BOOLEAN_EXACT['lookup_type'])

            elif attr.__class__ in BOOLEAN_EXACT['types']:
                result += TEMPLATE.format(
                    name=attr.name,
                    attr_name=attr.name,
                    filter_type=BOOLEAN_EXACT['filter_type'],
                    lookup_type=BOOLEAN_EXACT['lookup_type'])

            elif attr.__class__ in TIME_MAX_MIN['types']:
                result += TEMPLATE.format(
                    name='to_{0}'.format(attr.name),
                    attr_name=attr.name,
                    filter_type=TIME_MAX_MIN['filter_type'],
                    lookup_type=TIME_MAX_MIN['lookup_type']['max']
                )
                result += TEMPLATE.format(
                    name='from_{0}'.format(attr.name),
                    attr_name=attr.name,
                    filter_type=TIME_MAX_MIN['filter_type'],
                    lookup_type=TIME_MAX_MIN['lookup_type']['min']
                )

            elif attr.__class__ in DATE_MAX_MIN['types']:
                result += TEMPLATE.format(
                    name='to_{0}'.format(attr.name),
                    attr_name=attr.name,
                    filter_type=DATE_MAX_MIN['filter_type'],
                    lookup_type=DATE_MAX_MIN['lookup_type']['max']
                )
                result += TEMPLATE.format(
                    name='from_{0}'.format(attr.name),
                    attr_name=attr.name,
                    filter_type=DATE_MAX_MIN['filter_type'],
                    lookup_type=DATE_MAX_MIN['lookup_type']['min']
                )

            elif attr.__class__ in DATE_TIME_MAX_MIN['types']:
                result += TEMPLATE.format(
                    name='to_{0}'.format(attr.name),
                    attr_name=attr.name,
                    filter_type=DATE_TIME_MAX_MIN['filter_type'],
                    lookup_type=DATE_TIME_MAX_MIN['lookup_type']['max']
                )
                result += TEMPLATE.format(
                    name='from_{0}'.format(attr.name),
                    attr_name=attr.name,
                    filter_type=DATE_TIME_MAX_MIN['filter_type'],
                    lookup_type=DATE_TIME_MAX_MIN['lookup_type']['min']
                )

        # add meta
        result += "\n\n    " \
                  "class Meta:" \
                  "\n        model = {0}\n".format(model.__name__)

        print result