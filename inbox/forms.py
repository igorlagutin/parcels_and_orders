# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.forms import Form, ModelChoiceField, \
    ModelForm, widgets, ModelMultipleChoiceField
from inbox.models import Ticket, Deliver, Content


class UserModelChoiceField(ModelChoiceField):
    """display user lastname in select"""

    def label_from_instance(self, obj):
        return obj.last_name


class FilterForm(Form):
    """search form"""
    created_on = forms.DateField(
        required=False,

        label='date: ',
        widget=widgets.DateInput(format='%d/%m/%Y', attrs={
            'placeholder': 'гггг/мм/дд',
            'class': 'form-control visible-lg',
            'data-provide': 'datepicker',
            'data-date-format': 'dd/m/yyyy',
            'autocomplete': 'off'
        }))

    creator = UserModelChoiceField(
        required=False,
        queryset=User.objects.all(),
        widget=widgets.Select(attrs={
            'class': 'form-control'}))

    serial = forms.CharField(
        max_length=100,
        required=False,
        widget=widgets.TextInput(attrs={
            'placeholder': 'ТТН',
            'class': 'form-control'
        })
    )

    deliver = forms.ModelChoiceField(
        widget=widgets.Select(attrs={
                'class': 'form-control'
        }),
        queryset=Deliver.objects.all(),
        required=False
    )

    content = forms.ModelChoiceField(
        widget=widgets.Select(attrs={
                'class': 'form-control'
        }),
        queryset=Content.objects.all(),
        required=False,

    )

    sender = forms.CharField(
        max_length=100,
        required=False,
        widget=widgets.TextInput(attrs={
            'placeholder': 'Отправитель',
            'class': 'form-control visible-lg'
        })
    )

    is_received = forms.BooleanField(
        required=False,
        label='Показать принятые'
    )
