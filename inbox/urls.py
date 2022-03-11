from django.urls import path
from inbox.views import IndexView, StartpageView

urlpatterns = [
    path('', IndexView.as_view(), name="inbox"),
    path('', IndexView.as_view(), name="inbox_create"),
    path('<int:ticket_id>/detail/', IndexView.as_view(), name="inbox_detail"),
    path('', IndexView.as_view(), name="print"),
]
