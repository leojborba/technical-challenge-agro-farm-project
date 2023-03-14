from farm_base.models import Farm
from django_filters import FilterSet


class FarmFilter(FilterSet):

    class Meta:
        model = Farm
        fields = ['owner__name', 'owner__document', 'owner__document_type', 'name', 'municipality', 'state', 'id']
