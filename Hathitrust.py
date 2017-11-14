# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 10:12:35 2017

@author: cyg
"""
import os
import os.path
import requests
import threading
import time




Book = {
'name': '',
'type': 'pdf',
'id': 'mdp.39015030844818',
'orient': 0,
'size' : 100,
'seq': [0, 150],
'attachment': 0
}

import time
def DownloadFile(url, dst):
    print url
    print dst
    if os.path.exists(dst):
        return
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))
    response = requests.get(url, stream=True)
    status = response.status_code
    if status == 200:
        #total_size = int(response.headers['Content-Length'])
        with open(dst, 'wb') as of:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    of.write(chunk)
        time.sleep(3)



class Hathitrust:
    def __init__(self, workroot):

        #self.baseurl = "https://babel.hathitrust.org/cgi/imgsrv/download"
        self.baseurl = "https://babel.hathitrust.org/cgi/imgsrv"
        self.workroot = workroot
        self.books = []

    def download(self, book):
        #https://babel.hathitrust.org/cgi/imgsrv/download/pdf?id=mdp.39015030844818;orient=0;size=100;seq=13;attachment=0
        #https://babel.hathitrust.org/cgi/imgsrv/image?id=mdp.39015030844818;seq=15;width=680
        for page in range(book['seq'][0], book['seq'][1]):
            src = self.baseurl + ("/download%s?id=%s;orient=%s;size=%d;seq=%d;attachment=%d" %
            (book['type'], book['id'], book['orient'], book['size'], page, book['attachment']))
            dst = self.workroot + ( "/%s/%08d.%s" % (book['name'], page, book['type']))
            DownloadFile(src, dst)

    def download_png(self, page):
        #https://babel.hathitrust.org/cgi/imgsrv/image?id=mdp.39015030844818;seq=15;width=680
        for page in range(book['seq'][0], book['seq'][1]):
            src = self.baseurl + ("/image?id=%s;seq=%d;width=3502" %
            ( book['id'],  page))
            dst = self.workroot + ( "/%s/%08d.%s" % (book['name'], page, 'png'))
            DownloadFile(src, dst)

    def process(self):
        for book in books:
            self.download(book)

if __name__	== "__main__":
    down = Hathitrust("D:/Book")
    book = {'name': 'Dear Brutus','type': 'pdf','id': 'mdp.39015030844818',
'orient': 0,'size' : 100,'seq': [1, 160], 'attachment': 1}
    down.download_png(book)



