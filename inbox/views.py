from django.views.generic import TemplateView, FormView, UpdateView
from django.urls import reverse_lazy
from django.http import Http404
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from inbox.repozitory import TicketRepozitory
from inbox.filters import TicketFilter
from inbox.forms import TicketCreateEditForm, TicketViewDebitForm
from inbox.services import TicketService
from inbox.models import Ticket
from inbox.const import ONLY_AUTHOR_CAN_EDIT_POST_MESSAGE, TICKET_ALREADY_DEBITED_MESSAGE


class StartpageView(LoginRequiredMixin, TemplateView):
    template_name = "common/startpage.html"


class IndexView(LoginRequiredMixin, FilterView):
    paginate_by = 50
    context_object_name = "tickets"
    filterset_class = TicketFilter
    template_name = "inbox/index.html"

    def get_queryset(self, **kwargs):
        return TicketRepozitory.get_ticket_list()


class CreateTicketView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = "inbox.manager"
    template_name = 'inbox/inbox_create.html'
    form_class = TicketCreateEditForm
    success_url = reverse_lazy('inbox')

    def form_valid(self, form):
        created = TicketService(self.request).create(form)
        return super().form_valid(created)


class EditTicketView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "inbox.manager"
    model = Ticket
    template_name = 'inbox/inbox_edit.html'
    form_class = TicketCreateEditForm
    context_object_name = "ticket"
    success_url = reverse_lazy('inbox')

    def form_valid(self, form):
        edited = TicketService(self.request).edit(form)
        return super().form_valid(edited)

    def dispatch(self, request, *args, **kwargs):
        ticket = self.get_object()
        if ticket.creator != self.request.user:
            raise Http404(ONLY_AUTHOR_CAN_EDIT_POST_MESSAGE)
        if ticket.is_received:
            raise Http404(TICKET_ALREADY_DEBITED_MESSAGE)
        return super(EditTicketView, self).dispatch(request, *args, **kwargs)


class DetailDebitTicketView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "inbox.manager"
    model = Ticket
    template_name = 'inbox/inbox_detail.html'
    form_class = TicketViewDebitForm
    context_object_name = "ticket"
    success_url = reverse_lazy('inbox')

    def form_valid(self, form):
        debited = TicketService(self.request).debit(form)
        return super().form_valid(debited)
