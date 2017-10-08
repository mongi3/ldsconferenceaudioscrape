#!/usr/bin/env python

import argparse
import sys
import time

from BeautifulSoup import BeautifulSoup as bs
from urlparse import urljoin
import requests

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("conferenceURL", type=str, help="top level URL to conference, eg) 'https://www.lds.org/general-conference/2017/10?lang=eng'")
parser.add_argument("-n", "--dryrun", action="store_true", help="Dry run.  Don't actually download any audio")
args = parser.parse_args()


# Pull top level page and extract links to talks of all sessions
res = requests.get(args.conferenceURL)
res.raise_for_status()
soup = bs(res.text)
talklinkinfo = soup.findAll('a', attrs={'class':'lumen-tile__link'})
talklinks = [urljoin(args.conferenceURL,x['href']) for x in talklinkinfo]

# Go to page for each individual talk and download talk audio
for link in talklinks:
    time.sleep(1) # throttle scrape requests`
    res = requests.get(link)
    res.raise_for_status()
    soup = bs(res.text)
    audiolink = [x['href'] for x in soup.findAll('a') if 'mp3' in x.get('href','')]
    if len(audiolink) != 1:
        print 'WARNING: problem uniquely identifing audio link.  Skipping page at', link
        print audiolink
        continue
    # download file to current directory
    audiolink = audiolink[0]
    print 'Downloading ', audiolink
    if not args.dryrun:
        audioreq = requests.get(audiolink, stream=True)
        audioreq.raise_for_status()
        outpufn = audioreq.headers['Content-Disposition'].split('filename=')[1][1:-1]
        with open(outpufn, 'wb') as audiofile:
            for chunk in audioreq.iter_content(1024):
                audiofile.write(chunk)



