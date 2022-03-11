from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django_filters.views import FilterView
from inbox.repozitory import TicketRepozitory
from inbox.filters import TicketFilter


class StartpageView(TemplateView):
    template_name = "common/startpage.html"


class IndexView(FilterView):
    paginate_by = 50
    context_object_name = "tickets"
    filterset_class = TicketFilter
    template_name = "inbox/index.html"

    def get_queryset(self, **kwargs):
        return TicketRepozitory(self.request).get_ticket_list()
