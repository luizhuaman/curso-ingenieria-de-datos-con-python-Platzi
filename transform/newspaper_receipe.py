""" Clean the dataset """
import argparse
import hashlib
import logging
from urllib.parse import urlparse

import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _read_data(filename):
    logger.info('Reading file %s', filename)
    
    return pd.read_csv(filename)


def _extract_newspaper_uid(filename):
    logger.info('Extracting newspaper uid')
    newspaper_uid = filename.split('_')[0]
    
    logger.info('Newspaper uid detected: %s', newspaper_uid)
    
    return newspaper_uid


def _add_newspaper_uid_column(df, newspaper_uid):
    logger.info('Filling newspaper_uid with %s', newspaper_uid)
    df['newspaper_uid'] = newspaper_uid
    
    return df


def _extract_host(df):
    logger.info('Extracting host from urls')
    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)
    
    return df


def _fill_missing_titles(df):
    logger.info('Filling missing titles.')
    missing_titles_mask = df['title'].isna()
    
    missing_titles = (df[missing_titles_mask]['url']
                      .str.extract(r'(?P<missing_titles>[^/]+)$')
                      .applymap(lambda title: title.split('-'))
                      .applymap(lambda title_word_list: ' '.join(title_word_list))
                      )
    
    df.loc[missing_titles_mask, 'title'] = missing_titles.loc[:, 'missing_titles']
    
    return df


def _generate_uids_for_rows(df):
    logger.info('Generating uids for each row')
    uids = (df
            .apply(lambda row: hashlib.md5(bytes(row['url'].encode())), axis=1)
            .apply(lambda hash_object: hash_object.hexdigest())
            )

    df['uid'] = uids
    
    return df.set_index('uid')


def _remove_new_lines_from_body(df):
    logger.info('Removing new lines from body.')
    
    stripped_body = (df
                     .apply(lambda row: row['body'], axis=1)
                     .apply(lambda body: list(body))
                     .apply(lambda letters: list(map(lambda letter: letter.replace('\n', ' '), letters)))
                     .apply(lambda letters: ''.join(letters)))
    
    df['body'] = stripped_body
    
    return df


def _tokenize_column(df, column_name):
    stop_words = set(stopwords.words('spanish'))

    column_names = []
    if type(column_name) is not list:
        column_names.append(column_name)
    else:
        column_names = column_name

    logger.info(
        f'Tokenizing column(s) {[column for column in column_names]}')

    for column in column_names:
        df['n_token_'+column] = (df
                                 .dropna()
                                 .apply(lambda row: nltk.word_tokenize(row[column]), axis=1)
                                 .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens)))
                                 .apply(lambda tokens: list(map(lambda token: token.lower(), tokens)))
                                 .apply(lambda word_list: list(filter(lambda word: word not in stop_words, word_list)))
                                 .apply(lambda valid_word_list: len(valid_word_list)))

    return df


# noinspection PyShadowingNames
def main(filename):
    """ Funcion principal """
    logger.info('Starting cleaning process')
    
    df = _read_data(filename)
    print('Dataframe in firts step')
    print(df)
    
    newspaper_uid = _extract_newspaper_uid(filename)
    df = _add_newspaper_uid_column(df, newspaper_uid)
    df = _extract_host(df)
    df = _fill_missing_titles(df)
    df = _generate_uids_for_rows(df)
    df = _remove_new_lines_from_body(df)
    df = _tokenize_column(df, 'title')
    df = _tokenize_column(df, 'body')

    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='The path to the dirty data', type=str)
    
    arg = parser.parse_args()
    
    df = main(arg.filename)

    print(df)
    df.to_csv('cleaned_dataframe_el_universal.csv', sep='\t', encoding='utf-8')
