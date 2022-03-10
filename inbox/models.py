# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User




class Deliver(models.Model):
    """delivers who can ship parcels, foreign key for Ticket"""
    name = models.CharField(max_length=60)

    class Meta:
        verbose_name = "Перевозчик"
        verbose_name_plural = "Перевозчики"

    def __str__(self):
        return self.name


class Content(models.Model):
    """Type of parsel content, foreign key for Ticket"""
    name = models.CharField(max_length=60)

    class Meta:
        verbose_name = "Тип посылки"
        verbose_name_plural = "Типы посылок"

    def __str__(self):
        return self.name


class Ticket(models.Model):
    """Parcel ticket"""

    deliver = models.ForeignKey(Deliver, on_delete=models.PROTECT)
    serial = models.CharField(max_length=20, unique=True)
    quantity_of_places = models.IntegerField()
    sender = models.CharField(max_length=100, blank=True)
    is_received = models.BooleanField(default=False)
    notes = models.CharField(blank=True, max_length=2048)
    content = models.ForeignKey(Content, on_delete=models.PROTECT)
    creator = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="ticket_creator",
        on_delete=models.PROTECT)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True, editable=True)
    money = models.CharField(max_length=20, blank=True)
    debit_on = models.DateTimeField(
        editable=True,
        null=True,
        blank=True)
    debit_comment = models.CharField(blank=True, max_length=2048)
    debit_sign = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="ticket_debit_sign",
        on_delete=models.PROTECT)
    debit_sign_on = models.DateTimeField(
        editable=True,
        null=True,
        blank=True)
    driver_sign = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="ticket_driver_sign",
        on_delete=models.PROTECT)
    modified_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="ticket_modified_by",
        on_delete=models.PROTECT)

    nontracked = models.BooleanField(default=False)
    viewed = models.BooleanField(default=True)
    delivery_status = models.CharField(
        max_length=200,
        blank=True,
        null=True)
    delivery_destination = models.CharField(
        max_length=200,
        blank=True,
        null=True)

    class Meta:
        verbose_name = "Посылка"
        verbose_name_plural = "Посылки"
        permissions = (("manager", "Can view and edit tickets"), ("sklad", "sign product tickets"),
                       ("director", "see signed products"))

    def __str__(self):
        return self.serial