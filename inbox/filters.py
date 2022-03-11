import django_filters
from django_filters.widgets import LookupChoiceWidget
from inbox.models import Ticket

class TicketFilter(django_filters.FilterSet):

    class Meta:
        model = Ticket
        fields = {
            'deliver':['exact'],
            'serial':['icontains'],
            'content':['exact'],
            'is_received':['exact'],
            'sender':['icontains'],
            'creator':['exact'],
            'created_on':['exact'],
        }