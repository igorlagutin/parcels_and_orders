# -*- coding: utf-8 -*-

from django.forms import ModelForm, widgets
from inbox.models import Ticket



class TicketCreateEditForm(ModelForm):
    """crate and edit form"""

    class Meta:
        model = Ticket
        fields = [
            'deliver',
            'serial',
            'quantity_of_places',
            'sender',
            'content',
            'money',
            'is_received',
            'notes',
            'delivery_status',
            'delivery_destination'
        ]
        widgets = {
            'notes': widgets.Textarea(
                attrs={
                    'placeholder': 'Примечание',
                    'class': 'form-control'
                }),
            'deliver': widgets.Select(
                attrs={
                    'placeholder': 'Перевозчик',
                    'class': 'form-control',
                    'autofocus': True}),
            'quantity_of_places': widgets.NumberInput(
                attrs={
                    'class': 'form-control'
                }),
            'sender': widgets.TextInput(
                attrs={
                    'placeholder': 'Отправитель',
                    'class': 'form-control'
                }),
            'content': widgets.Select(
                attrs={
                    'placeholder': 'Что в посылке',
                    'class': 'form-control'
                }),
            'serial': widgets.TextInput(
                attrs={
                    'placeholder': 'ТТН',
                    'class': 'form-control'
                }),
            'status': widgets.CheckboxInput(
                attrs={
                    'class': 'form-control'
                }),
            'money': widgets.TextInput(
                attrs={
                    'placeholder': 'СУММА',
                    'class': 'form-control'
                }),
            'delivery_status': widgets.TextInput(
                attrs={
                    'type': 'hidden'
                }),
            'delivery_destination': widgets.TextInput(
                attrs={
                    'type': 'hidden'
                }),
        }
        labels = {
            'notes': 'Примечание',
            'deliver': 'Перевозчик *',
            'quantity_of_places': 'Количество мест *',
            'sender': 'Отправитель',
            'content': 'Что в посылке *',
            'serial': 'ТТН *',
            'is_received': 'Посылка принята?',
            'money': 'Сумма',
            'delivery_status': '',
            'delivery_destination': '',
        }


class TicketViewDebitForm(ModelForm):
    """view form"""
    class Meta:
        model = Ticket
        fields = ['debit_comment']
        widgets = {
            'debit_comment': widgets.Textarea(attrs={
                'placeholder': 'Примечание...',
                'class': 'form-control'}),
        }
        labels = {
            'debit_comment': 'Примечания при приходовании:',
        }