# cargo-duplicates-to-discord
Python script that checks a MediaWiki wiki's [Cargo](https://www.mediawiki.org/wiki/Extension:Cargo) tables for duplicate rows, prints the list of tables to console, and sends these results to a Discord webhook. Discord functionality may be easily commented out for users who wish to just run locally.

<img width="598" alt="Screen Shot 2021-06-11 at 12 45 48 AM" src="https://user-images.githubusercontent.com/7636606/121637011-5fe47680-ca4e-11eb-8002-626156d4b7ef.png">

Background: Cargo may sometimes insert duplicate rows in a table, requiring recreation. The current cause is unknown, but it may be due to a race condition or how a MediaWiki wiki's job queue is configured. As a stopgap for [Nookipedia](https://nookipedia.com/wiki/Main_Page), this script was made to run as a cron job to regularly inform Nookipedia editors when a table needs to be recreated.

# Configuration
The constants at the top of the file serve as the script's configurations.

**Integrations:**
* `WEBHOOK`: The URL of the Discord webhook to send to. Learn how to make a webhook [here](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks).
* `WIKI_DOMAIN`: Scheme and domain of the wiki e.g. `https://example.com`
* `WIKI_BASE_PATH`: [Base/script path](https://www.mediawiki.org/wiki/Manual:$wgScriptPath) of the wiki e.g. `/wiki/`
* `WIKI_API_PATH`: API path of the wiki e.g. `/w/api.php`

**Embed Configs:**
* `EMBED_DESCRIPTION`: Text at the top of the embed box.
* `EMBED_COLOR`: Decimal value of the embed color (this is the accent line that appears at the top of the embed box) e.g. `15158332` for red
* `EMBED_FOOTER`: Optional text to place at the bottom of the embed.
* `EMBED_THUMBNAIL`: Optional URL for a decorative image to display in the embed.

**Table metadata:**
* `TABLES`: A key/value dictionary of table names and their unique identifiers (primary key).

Example: if you have table `business_locations` and column `addresses` that contains what should be unique values, `TABLES` would look like:
```
{
  'business_locations': 'addresses'
}
```

If you have another table called `inventory`, and each item is uniquely identified by its `name` and `style`, you will have:
```
{
  'business_locations': 'addresses',
  'inventory': 'name,style'
}
```

**Other:**
* `SLEEP`: Seconds to sleep between Cargo queries.

# Technical details
This script works by querying the MediaWiki API's `cargoquery` endpoint. A Cargo table can be checked for duplicate values by querying for the primary key, grouping by those same keys, and having `COUNT(*) > 1`.
```
{
'action': 'cargoquery',
'format': 'json',
'limit': '500',
'tables': table,
'fields': TABLES[table],
'group_by': TABLES[table],
'having': 'COUNT(*)>1`
}
```

Depending on the wiki, a simpler implementation of this script could be to automatically pull all of a wiki's tables via `action=cargoqueryautocomplete` and checking each table for dupicate `_pageName`s. However, `_pageName` is not always a unique identifier if one page has multiple Cargo stores, nor may we want to check all tables, which is why this script is set up to require manually listing tables and values.
