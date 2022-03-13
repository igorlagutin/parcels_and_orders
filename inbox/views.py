from django.views.generic import TemplateView, FormView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.http import Http404
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from inbox.const import ONLY_AUTHOR_CAN_EDIT_POST_MESSAGE, TICKET_ALREADY_DEBITED_STATUS
from inbox.filters import TicketFilter
from inbox.forms import TicketCreateEditForm, TicketViewDebitForm

from inbox.repozitory import TicketDBRepozitory
from inbox.services import TicketService, ApiTicketService

from inbox.models import Ticket
from inbox.serializers import SerialDeliverSerializer


class StartpageView(LoginRequiredMixin, TemplateView):
    template_name = "common/startpage.html"


class IndexView(LoginRequiredMixin, FilterView):
    paginate_by = 50
    context_object_name = "tickets"
    filterset_class = TicketFilter
    template_name = "inbox/index.html"

    def get_queryset(self, **kwargs):
        return TicketDBRepozitory.get_ticket_list()


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
            raise Http404(TICKET_ALREADY_DEBITED_STATUS)
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


@method_decorator(csrf_exempt, name='dispatch')
class RefreshTicketStatusAPIView(LoginRequiredMixin, PermissionRequiredMixin, APIView):
    permission_required = "inbox.manager"

    def get(self, request, pk):
        repo = TicketDBRepozitory()
        return Response(repo.get_ticket_status_from_api(pk))

    def post(self, request, pk):
        repo = TicketDBRepozitory()
        return Response(repo.refresh_ticket_status_from_api(pk))


@method_decorator(csrf_exempt, name='dispatch')
class GetTicketStatusAPIView(LoginRequiredMixin, PermissionRequiredMixin, APIView):
    permission_required = "inbox.manager"

    def post(self, request):
        serializer = SerialDeliverSerializer(data=request.data)
        if serializer.is_valid():
            serial = serializer.validated_data['serial']
            deliver_name = serializer.validated_data['deliver_name']
            return Response(
                ApiTicketService.get_api_status_by_serial_and_deliver_name(
                    serial,
                    deliver_name))
        else:
            return Response(serializer.errors, status=400)
