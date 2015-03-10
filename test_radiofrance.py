#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from radiofrance import *

class KnownValues(unittest.TestCase):                          
    knownValuesContentId = (
        ( 'http://www.franceculture.fr/emission-le-tete-a-tete-sophie-calle-rediffusion-de-l-emission-du-30-septembre-2012-2013-08-18', 4654404),
        ( 'http://www.franceinter.fr/emission-la-bas-si-jy-suis-julian-assange-cyberterroriste-2', 590616),
        ( 'http://www.franceculture.fr/emission-sur-les-docks-polyandrie-23-%C2%AB-les-na-de-chine-le-fantasme-de-la-femme-liberee-%C2%BB-2014-03-05', 4803700),
        ( 'http://www.franceinter.fr/emission-a-ton-age-23-ans', 1011633),
        )

    knownValuesPodcast = (
        ( 'http://www.franceculture.fr/emission-le-tete-a-tete-sophie-calle-rediffusion-de-l-emission-du-30-septembre-2012-2013-08-18', 'http://www.franceculture.fr/sites/default/files/sons/2013/08/s33/RF_257BABE0-01E9-449D-AFF8-3A771876A60A_GENE.MP3'),
        ( 'http://www.franceinter.fr/emission-la-bas-si-jy-suis-julian-assange-cyberterroriste-2', 'http://www.franceinter.fr/sites/default/files/sons/2013/03/s12/NET_FI_c692194b-5f94-4e82-b906-9b839a4e12a6.mp3'),
        ( 'http://www.franceculture.fr/emission-sur-les-docks-polyandrie-23-%C2%AB-les-na-de-chine-le-fantasme-de-la-femme-liberee-%C2%BB-2014-03-05', 'http://www.franceculture.fr/sites/default/files/sons/2014/03/s10/RF_5D8BD372-5FEB-4ADC-A7AC-DB93DCD5E1C8_GENE.MP3' ),
        ( 'http://www.franceinter.fr/emission-a-ton-age-23-ans', 'http://www.franceinter.fr/sites/default/files/sons/2014/11/s48/net-fi-021610f6-8f7e-43f3-b97b-16d0a08fe8c1.mp3' ),
        )

    def testKnownValuesContentId(self):
        for page, content_id in self.knownValuesContentId:
            result = get_content_id_from_page(page)
            self.assertEqual(result, content_id)

    def testKnownValuesPodcast(self):
        for page, podcast in self.knownValuesPodcast:
            result = get_podcast(page)
            self.assertEqual(result, podcast)

if __name__ == "__main__":
    unittest.main()
