"""
News scrapper
"""

import argparse
import csv
import logging
import re
from datetime import datetime

from requests.exceptions import HTTPError
from urllib3 import HTTPSConnectionPool
from urllib3.exceptions import MaxRetryError

from common import config
import news_page_objects as news

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

is_well_formed_link = re.compile(r'^https?://.+/.+$')
is_root_path = re.compile(r'^/.+$')


def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return host + link
    else:
        return host + '/' + link


def _fetch_article(news_site_uid, host, link):
    logger.info('Start fetching article at %s' % link)
    
    article = None

    try:
        article = news.ArticlePage(news_site_uid, _build_link(host, link))
    except Exception as e:
        logger.warning('Error while fetching the article', exc_info=False)
        print('Exception: ', e)
        return None
        
    if article and not article.body:
        logger.warning('Invalid article. There is no body.')
        return None
    
    return article


def _save_articles(news_site_uid, articles):
    now = datetime.now().strftime('%Y_%m_%d')
    out_file_name = '%s_%s_articles.csv' % (news_site_uid, now)
    csv_headers = list(filter(lambda prop: not prop.startswith('_'), dir(articles[0])))
    
    print('\n\nCSV HEADERS', csv_headers)
    
    with open(out_file_name, mode='w+') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

        for article in articles:
            row = [str(getattr(article, prop)) for prop in csv_headers]
            writer.writerow(row)


def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']
    
    logging.info('Beginning scraper for %s' % host)
    homepage = news.HomePage(news_site_uid, host)
    
    articles = []
    count = 0
    for link in homepage.article_links:
        article = _fetch_article(news_site_uid, host, link)
        
        if article:
            logger.info('Article fetched!')
            articles.append(article)
            
            # for test.
            if count > 100:
                break
            count += 1

            # break
    
    _save_articles(news_site_uid, articles)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    news_sites_choices = list(config()['news_sites'].keys())
    parser.add_argument('news_site', help='The news sites that you want to scrape.', type=str,
                        choices=news_sites_choices)
    
    args = parser.parse_args()
    _news_scraper(args.news_site)
