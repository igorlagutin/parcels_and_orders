from django.urls import path
from django.contrib.auth.decorators import login_required
from inbox.views import IndexView, CreateTicketView, \
    EditTicketView, DetailDebitTicketView, RefreshTicketStatusAPIView, \
    GetTicketStatusAPIView

urlpatterns = [
    path('', IndexView.as_view(), name="inbox"),
    path('create/', CreateTicketView.as_view(), name="inbox_create"),
    path('<int:pk>/edit/', login_required(EditTicketView.as_view()), name="inbox_edit"),
    path('<int:pk>/detail/', DetailDebitTicketView.as_view(), name="inbox_detail"),
    path('', IndexView.as_view(), name="print"),
    path('<int:pk>/api/', RefreshTicketStatusAPIView.as_view(), name="inbox_api"),
    path('api/', GetTicketStatusAPIView.as_view(), name="inbox_api"),
]
