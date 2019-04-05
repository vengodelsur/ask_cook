# -*- coding: utf-8 -*-

# Scrapy settings for recipes_scrapers project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'recipes_scrapers'

SPIDER_MODULES = ['recipes_scrapers.spiders']
NEWSPIDER_MODULE = 'recipes_scrapers.spiders'

SELECTORS = {'edimdoma.ru': {'recipe_title': 'h1.recipe-header__name::text',
                             'ingredient_section': 'div.field-row.recipe_ingredients',
                             'ingredient_section_name':'div.section-title::text',
                             'ingredient': 'table.definition-list-table',
                             'ingredient_name': 'span.recipe_ingredient_title::text',
                             'ingredient_amount': 'td.definition-list-table__td.definition-list-table__td_value::text',
                             'step': 'div.plain-text.recipe_step_text::text'},
             'eda.ru': {'recipe_title': 'h1.recipe__name::text',
                        'ingredient': 'p::attr(data-ingredient-object)',
                        'step': 'span.instruction__description::text'},
             'say7.info': {'recipe_title': '[itemprop="name"]::text',
                           'ingredient': '[itemprop="recipeIngredient"]::text',
                           'step': '[itemprop="recipeInstructions"] p::text'}}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'recipes_scrapers (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'recipes_scrapers.middlewares.RecipesScrapersSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'recipes_scrapers.middlewares.RecipesScrapersDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'recipes_scrapers.pipelines.RecipesScrapersPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
