import pytest
import json

from django.test import Client


pytestmark = [pytest.mark.django_db]


def test_create_farm_ok(client: Client, owner):
    payload = {
        'name': 'Fazenda',
        'municipality': 'Floripa',
        'state': 'Santa Catarina',
        'owner': owner.id,
        'geometry': json.dumps({
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
    }

    response = client.post(path='/api/v1/farms', data=payload)

    assert response.status_code == 201
    assert json.loads(response.content) == {
        'id': 1,
        'name': 'Fazenda',
        'geometry': {'type': 'Polygon', 'coordinates': [[[-37.5238037109375, -10.93984346235492],
                                                         [-37.48260498046874, -11.02073244690711],
                                                         [-37.43728637695312, -10.94658505651706],
                                                         [-37.5238037109375, -10.93984346235492]]]},
        'centroid': {'type': 'Point', 'coordinates': [-37.48123168945313, -10.969053655259698]},
        'area': 0.003360277085671756,
        'municipality': 'Floripa',
        'state': 'Santa Catarina',
        'owner': 1
    }


def test_list_farm_id_ok(client: Client, farm):
    response = client.get(path=f'/api/v1/farms/{farm.id}')

    assert response.status_code == 200

    content = json.loads(response.content)
    assert content['id'] == 1
    assert content['owner'] == {
        'id': 1,
        'name': 'Leo Borba',
        'document': '99999999999',
        'document_type': 'CPF'
    }
    assert content['name'] == 'Fazenda'
    assert content['geometry'] == {'type': 'Polygon', 'coordinates': [[[-37.5238037109375, -10.93984346235492],
                                                                       [-37.48260498046874, -11.02073244690711],
                                                                       [-37.43728637695312, -10.94658505651706],
                                                                       [-37.5238037109375, -10.93984346235492]]]}
    assert content['area'] == 0.01
    assert content['centroid'] == {'coordinates': [-5.375419239857919, 26.91253738736171], 'type': 'Point'}
    assert content['municipality'] == 'Floripa'
    assert content['state'] == 'Santa Catarina'


def test_list_farm_filters_ok(client: Client, farm):
    response = client.get(path=f'/api/v1/farms?owner__name={farm.owner.name}&owner__document={farm.owner.document}&'
                               f'owner__document_type={farm.owner.document_type}&name={farm.name}&'
                               f'municipality={farm.municipality}&state={farm.state}')

    assert response.status_code == 200
    assert json.loads(response.content) == [{
        'area': 0.01,
        'centroid': {'coordinates': [-5.375419239857919, 26.91253738736171], 'type': 'Point'},
        'municipality': 'Floripa',
        'name': 'Fazenda',
        'owner': 1,
        'state': 'Santa Catarina'
    }]


def test_farm_fail_restrictions(client: Client):
    payload = {
        'geometry': json.dumps({
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
    }

    response = client.post(path='/api/v1/farms', data=payload)

    assert response.status_code == 400
    assert json.loads(response.content) == {
        'name': ['This field is required.'],
        'municipality': ['This field is required.'],
        'state': ['This field is required.'],
        'owner': ['This field is required.']
    }
