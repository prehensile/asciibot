from bs4 import BeautifulSoup
import random
import urllib2
import re
import logging
import twitterconnector

class AsciiBot( object ):

    def run( self, do_tweet=True, twitter_creds_path=None ):

        root_url = "http://textfiles.com"
        root_paths = [ "100", "adventure", "apple", "bbs",
        "computers", "conspiracy", "drugs", "etext", "food", "fun", "games", "groups",
        "hacking", "hamradio", "holiday", "humor", "internet", "law", "magazines",
        "media", "messages", "music", "news", "occult", "phreak", "piracy", "politics",
        "programming", "reports", "rpg", "science", "sex", "sf", "stories", "survival",
        "ufo", "uploads", "virus" ]

        tweet = None
        safety = 10
        current_url = None
        current_file = None
        re_endpunctuation = re.compile("[.?!]+")
        tweet_minlength = 15
        tweet_maxlength = 140
        while tweet is None and safety > 0:
            
            if current_url is None:
                current_url = "%s/%s" % (root_url,random.choice( root_paths )) 

            response = None
            try:
                response = urllib2.urlopen( current_url )
                info = response.info()
                content_type = info[ "Content-type" ]
            except urllib2.HTTPError, e:
                logging.info( e )

            if response is None:
                current_url = None

            elif content_type == "text/plain":
            
                shortened_response = urllib2.urlopen(  "http://is.gd/create.php?format=simple&url=%s" % current_url )
                shortened_url = shortened_response.read()
               
                text_file = response.read()

                tweet_safety = 10
                while tweet is None and tweet_safety > 0:
                    matches = list( re_endpunctuation.finditer( text_file ) )
                    if len(matches) > 1:
                        match_ptr = random.randint(0,len(matches)-2)
                        match_start = matches[ match_ptr ]
                        match_end = matches[ match_ptr + 1 ]
                        extract = text_file [ match_start.end() : match_end.end() ]
                        extract = extract.lstrip()
                        
                        not_words = re.findall( "[^a-zA-Z0-9]", extract )
                        # only continue if extract has a reasonable amount of alphanumerics
                        # (not a bunch of punctuation/whitespace)
                        if len( not_words ) < len( extract )* 0.3 and '"' not in extract: # supporting quotes is a PITA
                            # refornat extract
                            out = ""
                            lines = extract.split("\n")
                            for line in lines:
                                line = line.rstrip( "\r -\t" ) # remove carriage returns, whitespace and hyphens
                                line = line.lstrip( "> \t-" ) # remove wonky formatting
                                if len(out)>0:
                                    out = "%s %s" % (out,line)
                                else:
                                    out = line
                            out = re.sub( "\s+", " ", out ) # collapse more than one space down to just one
                            l = len(out)
                            if l in xrange( tweet_minlength, 137 - len(shortened_url) - len(current_file) ):
                                tweet = "%s // %s %s" % ( out, current_file.upper(), shortened_url )
                    tweet_safety -= 1
                if tweet_safety < 1:
                    current_url = None
            
            elif content_type == "text/html":
                html = response.read()
                soup = BeautifulSoup( html )
                links = soup.find_all( "a" )
                
                link = None
                href = None
                while href is None:
                    link = random.choice( links )
                    href = link.attrs[ "href" ]
                    # skip links to things not in the current directory
                    if href.startswith( "http://"):
                        href = None

                current_file = href 
                current_url = "%s/%s" % (current_url,href)

            else:
                current_url = None

            safety -=1

        if tweet is not None:
            logging.info( tweet )
            if do_tweet and twitter_creds_path:
                twitter_connector = twitterconnector.TwitterConnector( twitter_creds_path )
                twitter_connector.tweet( tweet )
