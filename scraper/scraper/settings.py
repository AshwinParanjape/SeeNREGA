# Scrapy settings for scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import sys
sys.path.append('/home/synerg/virtualenv/nrega/SeeNREGA/storeNrega/')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'storeNrega.settings'

BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scraper (+http://www.yourdomain.com)'

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = True
