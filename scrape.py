#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup as bs
from urlparse import urljoin
import requests

baseurl = 'https://www.lds.org/general-conference?cid=HP_SA_23-9-2017_dGC_fBCAST_xLIDyL1-B_&lang=eng'
res = requests.get(baseurl)
res.raise_for_status()

soup = bs(res.text)
links = soup.findAll('a')
tmp = [urljoin(baseurl, x['href']) for x in links if 'general-conference/2017/10/' in x.get('href','')]


for link in tmp:
    res = requests.get(link)
    res.raise_for_status()
    soup = bs(res.text)
    audiolink = [x['href'] for x in soup.findAll('a') if 'mp3' in x.get('href','')]
    if len(audiolink) != 1:
        print 'WARNING: problem uniquely identifing audio link'
        print audiolink
        continue
    # download file to current directory
    audiolink = audiolink[0]
    print 'grabbing ', audiolink
    audioreq = requests.get(audiolink)
    audioreq.raise_for_status()
    outpufn = audioreq.headers['Content-Disposition'].split('filename=')[1][1:-1]
    with open(outpufn, 'wb') as audiofile:
        for chunk in audioreq.iter_content(100000):
            audiofile.write(chunk)


