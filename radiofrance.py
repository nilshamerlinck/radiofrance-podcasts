#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs, locale, os, sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

import httplib
import urllib2 
from cookielib import CookieJar
import urlparse
import os.path

import re

VERBOSE = False
OPENER = None

def get_opener():
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [ 
        ('Content-type', 'application/x-www-form-urlencoded'),
        ('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'),
        ('Accept', 'text/plain, text/html')
        ]

    return opener

def get_podcast(page):
    netloc = urlparse.urlsplit(page).netloc # ex: www.franceculture.fr

    global OPENER
    if not OPENER:
        OPENER = get_opener()

    content_id = get_content_id_from_page(page)
    if VERBOSE:
        print content_id

    iframe = 'http://%s/player/export-reecouter?content=%s' % (netloc, content_id)

    if VERBOSE:
        print iframe
    
    data = get_data_from_iframe(iframe)
    
    podcast = data['url']
    output_file = data['output_file']

    if VERBOSE:
        print 'wget -O %s "%s"' % (
            output_file,
            podcast)

    return podcast

def get_content_id_from_page(page):
    global OPENER
    if not OPENER:
        OPENER = get_opener()

    resp = OPENER.open(page)
    c = resp.read().decode('utf-8')

    RE_CONTENT_ID = re.compile(r'href="/player/reecouter\?play=(?P<content_id>\d+)"', re.UNICODE)
    m = RE_CONTENT_ID.findall(c)
    if not m:
        return None
    if len(m) == 1:
        m = m[0]
    else:
        """
        éviter le journal
        ex: http://www.franceinter.fr/emission-a-ton-age-23-ans
        """

        m = m[1]

    content_id = int(m)

    return content_id    

def get_data_from_iframe(iframe):
    global OPENER
    if not OPENER:
        OPENER = get_opener()

    resp = OPENER.open(iframe)
    c = resp.read().decode('utf-8')

    data = {}

    """
    ex: http://www.franceculture.fr/emission-sur-les-docks-polyandrie-23-%C2%AB-les-na-de-chine-le-fantasme-de-la-femme-liberee-%C2%BB-2014-03-05
    """
        
    RE_URL = re.compile(r'<a id="player-link" href="(?P<url>[^"]+)"')
    m = RE_URL.search(c)

    if m:
        data['url'] = m.group('url')

        RE_MORE = re.compile(r'<a href="/(?P<more>[^"]+)" class="more" target="_blank">', re.UNICODE)
        m = RE_MORE.search(c)
    
        data['output_file'] = '%s.mp3' % m.group('more')
    else:
        """
        autre cas de figure : chronique dans une émission
        ex: http://www.franceinter.fr/emission-a-ton-age-23-ans
        """
        
        RE_URL = re.compile(r'<a id="player" data-diffusion-id="" href="(?P<url>[^"]+)"')
        m = RE_URL.search(c)
        data['url'] = m.group('url')

        RE_MORE = re.compile(r'<span class="path-diffusion">/(?P<more>.+)</span>')
        m = RE_MORE.search(c)

        data['output_file'] = '%s.mp3' % m.group('more')

    return data

def main():
    global VERBOSE

    from optparse import OptionParser

    usage="""
%prog [ options ]

Exemple:

$ python radiofrance.py http://www.franceculture.fr/emission-le-tete-a-tete-sophie-calle-rediffusion-de-l-emission-du-30-septembre-2012-2013-08-18
  """[1:-3]
    
    parser = OptionParser(usage=usage)
    parser.add_option('--verbose',
                      help='verbose',
                      default=VERBOSE,
                      action='store_true',
                      dest='verbose')

    options, args = parser.parse_args()

    VERBOSE = options.verbose

    if not args:
        print usage

    for arg in args:
        print get_podcast(arg)

if __name__ == '__main__':
    sys.exit(main())
