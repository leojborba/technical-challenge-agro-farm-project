import json
import factory

from farm_base.models.owner import Owner
from farm_base.models.farm import Farm


class OwnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Owner

    name = 'Leo Borba'
    document = '99999999999'
    document_type = 'CPF'


class FarmFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Farm

    name = 'Fazenda'
    municipality = 'Floripa'
    state = 'Santa Catarina'
    owner = factory.SubFactory(OwnerFactory)
    area = 0.01
    geometry = json.dumps({
        'type': 'Polygon',
        'coordinates': [
            [
                [
                    -10.93984346235492,
                    -37.5238037109375
                ],
                [
                    -11.02073244690711,
                    -37.48260498046874
                ],
                [
                    -10.94658505651706,
                    -37.43728637695312
                ],
                [
                    -10.93984346235492,
                    -37.5238037109375
                ]
            ]
        ]
    })
    centroid = json.dumps({
        'type': 'Point',
        'coordinates': [
            26.91253738736171,
            -5.375419239857919
        ]
    })
