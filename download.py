import json
import logging
import os
import requests
import shutil

with open('download.log', 'w'):
    pass

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler('download.log')
handler.setLevel(logging.INFO)
logger.addHandler(handler)

def download_emotes(emote_list):
    TEMPLATE = "http://static-cdn.jtvnw.net/emoticons/v1/{image_id}/1.0"

    for key, value in emote_list.iteritems():
        url = TEMPLATE.format(image_id=value['image_id'])
        path = './global/{id}.png'.format(id=key)

        r = requests.get(url, stream=True)
        if r.status_code == 200:
            logger.info('Saving image to {path}'.format(path=path))
            with open(path, 'wb') as file:
                for chunk in r.iter_content():
                    file.write(chunk)
        logger.info('Finished downloading emotes')

def get_emote_list():
    EMOTE_LIST_URL = "http://twitchemotes.com/api_cache/v2/global.json"

    logger.info('Requesting emote list from {0}'.format(EMOTE_LIST_URL))
    resp = requests.get(EMOTE_LIST_URL)

    if (resp.status_code != 200):
        logger.error('Cannot get emote list. Status code={0}'.format(resp.status_code))
    else:
        r_json = resp.json()
        return r_json['emotes']
        download_emotes(r_json['emotes'])

emote_list = get_emote_list()
download_emotes(emote_list)
