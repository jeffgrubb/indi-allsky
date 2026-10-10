from urllib.parse import parse_qs

import pytest

from indi_allsky import constants
from indi_allsky.s3_tags import build_object_tagging, build_object_tags


@pytest.mark.parametrize('asset_type, expected', list(constants.ASSET_TYPE_NAMES.items()))
def test_build_object_tags_maps_asset_types(asset_type, expected):
    assert build_object_tags({'type': asset_type}) == {
        'indi-allsky:asset-type': expected,
    }


@pytest.mark.parametrize('night, expected', [(True, 'night'), (False, 'day')])
def test_build_object_tags_maps_timeofday(night, expected):
    tags = build_object_tags({
        'type': constants.IMAGE,
        'night': night,
    })

    assert tags['indi-allsky:timeofday'] == expected


def test_build_object_tags_includes_asset_context():
    tags = build_object_tags({
        'type': constants.THUMBNAIL,
        'origin': constants.STARTRAIL,
        'night': True,
        'dayDate': '20261010',
        'camera_uuid': '58fda4fd-4b79-43e3-a88a-b27048e84775',
    })

    assert tags == {
        'indi-allsky:asset-type': 'thumbnail',
        'indi-allsky:timeofday': 'night',
        'indi-allsky:day-date': '20261010',
        'indi-allsky:camera-uuid': '58fda4fd-4b79-43e3-a88a-b27048e84775',
        'indi-allsky:origin': 'startrail',
    }


@pytest.mark.parametrize('metadata', [None, {}, {'type': -1}, 'image'])
def test_build_object_tags_ignores_unknown_metadata(metadata):
    assert build_object_tags(metadata) == {}
    assert build_object_tagging(metadata) == ''


def test_build_object_tagging_is_url_encoded_for_boto3():
    tagging = build_object_tagging({
        'type': constants.THUMBNAIL,
        'origin': constants.IMAGE,
        'night': False,
    })

    assert parse_qs(tagging) == {
        'indi-allsky:asset-type': ['thumbnail'],
        'indi-allsky:timeofday': ['day'],
        'indi-allsky:origin': ['image'],
    }
