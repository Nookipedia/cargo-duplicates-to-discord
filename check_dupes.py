# Query a MediaWiki wiki's Cargo tables for duplicate rows and sends the results to a Discord webhook.
# Populate constants to run.
# @author Kevin Payravi (SuperHamster)

import requests
import json
from time import sleep

WEBHOOK = 'https://discord.com/api/webhooks/{webhook.id}/{webhook.token}' # INSERT DISCORD WEBHOOK URL HERE
WIKI_DOMAIN = 'https://nookipedia.com'
WIKI_BASE_PATH = '/wiki/'
WIKI_API_PATH = '/w/api.php'
EMBED_DESCRIPTION = "GRAAAH! We've got some Cargo tables with duplicate rows. Will a Cargo Technician please [recreate](" + WIKI_DOMAIN + WIKI_BASE_PATH + "Special:CargoTables) these?"
EMBED_COLOR = '14250002'
EMBED_FOOTER = 'Got it? NOW SCRAM!'
EMBED_THUMBNAIL = 'https://dodo.ac/np/images/e/e0/Cargo_logo_cropped.png'
SLEEP = 2 # Seconds to sleep between Cargo queries
TABLES = {
    'amiibo_card': 'number',
    'cf_art': 'name',
    'cf_bug': 'name',
    'cf_fish': 'name',
    'cf_house': 'villager',
    'cf_villager': 'name',
    'e_card': 'number',
    'furniture_collection': 'url',
    'hhd_villager': 'name',
    'nh_art': 'name',
    'nh_bug': 'name',
    'nh_calendar': 'date,event',
    'nh_clothing': 'en_name',
    'nh_clothing_variation': 'en_name,variation',
    'nh_distribution': 'en_name',
    'nh_fish': 'name',
    'nh_fossil': 'name',
    'nh_fossil_group': 'name',
    'nh_furniture': 'en_name',
    'nh_furniture_variation': 'en_name,variation,pattern',
    'nh_house': 'villager',
    'nh_interior': 'en_name',
    'nh_item': 'en_name',
    'nh_language_name': 'en_name',
    'nh_music': 'en_name',
    'nh_photo': 'en_name',
    'nh_photo_variation': 'en_name,variation',
    'nh_recipe': 'en_name',
    'nh_sea_creature': 'name',
    'nh_tool': 'en_name',
    'nh_tool_variation': 'en_name,variation',
    'nh_villager': 'name',
    'nl_art': 'name',
    'nl_bug': 'name',
    'nl_fish': 'name',
    'nl_house': 'villager',
    'nl_sea_creature': 'name',
    'nl_villager': 'name',
    'nlwa_rv': 'name,interior_image',
    'pc_furniture': 'en_name',
    'pc_recipe': 'en_name',
    'pc_recipe_reissue': 'en_name',
    'pc_villager': 'name',
    'pg_bug': 'name',
    'pg_clothing': 'en_name',
    'pg_fish': 'name',
    'pg_fossil': 'name',
    'pg_furniture': 'en_name,in_dnm,in_plus,in_pg,in_e_plus',
    'pg_house': 'villager',
    'pg_interior': 'en_name',
    'pg_item': 'en_name',
    'pg_language_name': 'en_name,de_name,es_name,fr_name,it_name,ja_name',
    'pg_umbrella': 'en_name',
    'pg_villager': 'name',
    'song': 'name',
    'special_character': 'name',
    #'ssbu_spirit': 'name', # Commented out due to valid duplicates
    'villager': 'url',
    'ww_house': 'villager',
    'ww_villager': 'name'
}

results = ''

try:
    for table in TABLES:
        fields = TABLES[table].replace('_pageName', '_pageName=pageName')
        group_by = TABLES[table].replace('_pageName', 'pageName')
        dupes = requests.get(url = WIKI_DOMAIN + WIKI_API_PATH, params = {'action': 'cargoquery', 'format': 'json', 'limit': '500', 'tables': table, 'fields': fields, 'group_by': group_by, 'having': 'COUNT(*)>1'}).json()
        if dupes['cargoquery']:
            results += table + ' - ' + str(len(dupes['cargoquery'])) + ' dupe(s)\n'
        sleep(SLEEP)

    if results:
        print(results)
        payload = {
            "embeds": [
                {
                    "description": EMBED_DESCRIPTION,
                    "color":  EMBED_COLOR,
                    "thumbnail": {
                        "url": EMBED_THUMBNAIL
                    },
                    "fields": [
                        {
                            "name": "Tables with duplicate rows:",
                            "value": results,
                            "inline": "true"
                        }
                    ],
                    "footer": {
                        "text": EMBED_FOOTER
                    }
                }
            ]
        }

        print('Discord webhook status: ' + str(requests.post(WEBHOOK, json = payload).status_code))
    else:
        print('No duplicates found!')

except Exception as e:
    print(e)
    pass
