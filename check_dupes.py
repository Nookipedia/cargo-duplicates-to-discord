# Query a MediaWiki wiki's Cargo tables for duplicate rows and sends the results to a Discord webhook.
# Populate constants to run.
# @author Kevin Payravi (SuperHamster)

import requests
import json
from time import sleep

WEBHOOK = 'https://discord.com/api/webhooks/{webhook.id}/{webhook.token}'
WIKI_DOMAIN = 'https://example.com'
WIKI_BASE_PATH = '/wiki/'
WIKI_API_PATH = '/w/api.php'
EMBED_DESCRIPTION = "Duplicate rows have been found in the wiki's [Cargo tables](" + WIKI_DOMAIN + WIKI_BASE_PATH + "Special:CargoTables)."
EMBED_COLOR = '15158332'
EMBED_FOOTER = ''
EMBED_THUMBNAIL = ''
SLEEP = 2 # Seconds to sleep between Cargo queries
TABLES = { # Populate with names of tables to check; value is columns that make up the table's unique identifier
    'table': 'column,column2'
}

results = ''

try:
    for table in TABLES:
        dupes = requests.get(url = WIKI_DOMAIN + WIKI_API_PATH, params = {'action': 'cargoquery', 'format': 'json', 'limit': '500', 'tables': table, 'fields': TABLES[table], 'group_by': TABLES[table], 'having': 'COUNT(*)>1'}).json()
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

        print('Discord webhook status: ' + requests.post(WEBHOOK, json = payload).status_code)
    else:
        print('No duplicates found!')

except Exception as e:
    print(e)
    pass
