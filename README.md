SeeNREGA
========

A webservice which allows rich queries to be executed and visualizations to be generated on India's NREGA data obtained by periodically crawling its website

Prerequisites 
-------------
* python python-dev
* pip
* mysql-server libmysqlclient-dev
* virtualenv (optional)
* git (to get the lastest versions and contribute)

Scraper
-------
This is a scrapy project which links to the database through django models.

"links" spider found in spiders/link_spider.py is responsible for populating the state, district, block and panchayat names and codes. It also populates the links which are used in other spiders.

"block_data" spider found in block_data_spider.py takes links to each block from the database and scrapes the tables for that block as defined in file scraperConfig.py 

scraperConfig.py contains 

1. Global start url for "links" spider
2. xpaths to extract names of districts, blocks and panchayats from state, district, block level pages respectively
3. blockDataConfig which is a dictionary, where the link text (as seen on website) is the key and the value is another dictionary (columnMappings)

   Column mappings dictionary maps column number in the correspoding table to attributes in the panchayat model
4. query attributes: these are strings which are used to extract data from queries which are a part of the request url and contains important information (eg. state_code etc)

storeNrega
-----------
This is a Django project containing nregaApp which contains models for storing data. 
