# flow
"""
1. 덤프 파일 다운로드 <<<
2. 텍스트 추출/Normalization
3. Tokenization
4. train embedding
"""
import argparse
from bs4 import BeautifulSoup
import os
import requests
import shutil


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--corpus', required=True, help='target corpus to download')
args = parser.parse_args()


class DownloadDump:
    """
    Download dump file of requested corpus.
    """

    def __init__(self, corpus):
        self.corpus = corpus
        self._urls = {
            'wiki': 'https://dumps.wikimedia.org/kowiki/latest/kowiki-latest-pages-articles-multistream.xml.bz2',
            'namuwiki': 'https://mu-star.net/wikidb#namu_new',
        }
        # dir_name = 'corpus'
        # if not os.path.exists(dir_name):
        #     os.makedirs(dir_name)
        # else:
        #     self.download_path = dir_name
        self.download_url = self._get_download_url()

    def _get_download_url(self):
        """
        Return a download url.
        """
        if self.corpus == 'wiki':
            download_url = self._urls[self.corpus]
        elif self.corpus == 'namuwiki':
            download_url = self._get_namuwiki_down_url()
        else:
            raise ValueError('Corpus must be wiki or namuwiki.')
        return download_url

    def _get_namuwiki_down_url(self):
        """
        Return a namuwiki download url.
        """
        base_url = self._urls['namuwiki']
        res = requests.get(base_url)
        # while res.status_code == 521:
        #     res = requests.get(base_url)

        contents = BeautifulSoup(res.content, 'html.parser')
        table = contents.find_all('table', 'table')
        namuwiki_down_url = table[0].find_all('tbody')[1].find_all('a')[1]['href']

        for a in table[0].find_all('tbody')[1].find_all('a'):
            if a.text == 'Download':
                namuwiki_down_url = a['href']
        return namuwiki_down_url

    def maybe_download(self):
        """
        Start download.
        """
        dir_path = 'corpus'

        file_name = self.download_url.split('/')[-1]
        download_path = os.path.join(dir_path, file_name)

        r = requests.get(self.download_url, stream=True)

        if os.path.exists(download_path):
            print('File found at {}, size: {}'.format(
                download_path, os.stat(download_path).st_size))
        else:
            # TODO: showing progress bar.
            os.makedirs(dir_path)
            with open(download_path, 'wb') as f:
                print('File not found. Start download...')
                shutil.copyfileobj(r.raw, f)

        return file_name


if __name__ == '__main__':
    download_dump = DownloadDump(args.corpus)
    download_dump.maybe_download()
