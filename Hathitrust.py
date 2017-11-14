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


def DownloadFile(url, dst):
    print url
    print dst
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))

    if os.path.exists(dst):
        return 1
    import urllib3
    urllib3.disable_warnings()
    response = requests.get(url, stream=True, verify=False)
    status = response.status_code
    if status == 200:
        #total_size = int(response.headers['Content-Length'])
        with open(dst, 'wb') as of:
            for chunk in response.iter_content(chunk_size=512):
                if chunk:
                    of.write(chunk)
        of.close()
    del response

    if os.path.exists(dst):
        return 1
    else:
        return 0


class Hathitrust:
    def __init__(self, workroot):
        self.baseurl = "https://babel.hathitrust.org/cgi/imgsrv"
        self.workroot = workroot
        self.books = self.loadbooks()

    def loadbooks(self):
        import json
        filepath = os.path.join(self.workroot, "hathitrust.json")
        return json.load(file(filepath))['Books']

    def run(self):
        for book in self.books:
            self.process(book)

    def process(self, book):
        print "process " + book['name']
        self.download_pages(book)
        self.pages2pdf(book)
        print book['name'] + " is ok!!!"

    def download_pages(self, book):
        #https://babel.hathitrust.org/cgi/imgsrv/download/pdf?id=mdp.39015030844818;orient=0;size=100;seq=13;attachment=0
        #https://babel.hathitrust.org/cgi/imgsrv/image?id=mdp.39015030844818;seq=15;width=680
        while True:
            num = 0
            for page in range(1, book['pages'] + 1):
                num += int(self.download_pdf(book, page))

            if num == int(book['pages']):
                break
    def pages2pdf(self, book):
        from pyPdf import PdfFileWriter, PdfFileReader
        output = PdfFileWriter()
        pages = book['pages']
        outputPages = 0
        for page in range(1, pages + 1):
            filepath = os.path.join(self.workroot, book['name'], "%08d.pdf" %  page)
            ifstr = PdfFileReader(file(filepath,"rb"))
            pageCount = ifstr.getNumPages()
            outputPages += pageCount
            for iPage in range(0,pageCount):
                output.addPage(ifstr.getPage(iPage))

        outfile = os.path.join(self.workroot, book['name'] + ".pdf")
        print outfile
        outputStream=file(outfile,"wb")
        output.write(outputStream)
        outputStream.close()
        print book['name'] + ".pdf is ok"

    def download_png(self, book, page):
        #https://babel.hathitrust.org/cgi/imgsrv/image?id=mdp.39015030844818;seq=15;width=680
        for page in range(1, book['pages'] + 1):
            src = self.baseurl + ("/image?id=%s;seq=%d;width=680" %
            ( book['id'],  page))
            dst = self.workroot + ( "/%s/%08d.%s" % (book['name'], page, 'png'))
            DownloadFile(src, dst)

    def download_pdf(self, book, page):
        src = self.baseurl + ("/download/pdf?id=%s;orient=0;size=100;seq=%d;attachment=0" %
            (book['id'], page))
        dst = self.workroot + ( "/%s/%08d.%s" % (book['name'], page, "pdf"))
        return DownloadFile(src, dst)

if __name__	== "__main__":
    down = Hathitrust(os.getcwd())
    down.run()



