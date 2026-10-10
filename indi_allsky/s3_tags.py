from urllib.parse import urlencode

from . import constants


def build_object_tags(metadata):
    if not isinstance(metadata, dict):
        return {}


    asset_type = constants.ASSET_TYPE_NAMES.get(metadata.get('type'))
    if not asset_type:
        return {}


    tags = {
        'indi-allsky:asset-type' : asset_type,
    }


    night = metadata.get('night')
    if isinstance(night, bool):
        tags['indi-allsky:timeofday'] = 'night' if night else 'day'


    day_date = metadata.get('dayDate')
    if isinstance(day_date, str) and day_date:
        tags['indi-allsky:day-date'] = day_date


    camera_uuid = metadata.get('camera_uuid')
    if isinstance(camera_uuid, str) and camera_uuid:
        tags['indi-allsky:camera-uuid'] = camera_uuid


    origin = constants.ASSET_TYPE_NAMES.get(metadata.get('origin'))
    if origin:
        tags['indi-allsky:origin'] = origin


    return tags


def build_object_tagging(metadata):
    return urlencode(build_object_tags(metadata))
