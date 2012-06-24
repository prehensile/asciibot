import tweepy
import os

class TwitterConnector( object ):

    def __init__( self, creds_path ):
        self.creds_path = creds_path
        self._api = None

    def api( self ):
        if (self._api is None) and (self.creds_path is not None):
            error = None
            
            try:
                fh = open( os.path.join( self.creds_path, 'consumer_token' ), 'r' )
                consumer_key, consumer_secret = fh.read().split("\n")
                fh.close()
            except IOError, e:
                error = e

            try: 
                fh = open( os.path.join( self.creds_path, 'access_token' ), 'r' )
                key, secret = fh.read().split("\n")
                fh.close()
            except IOError, e:
                error = e

            if error is None:
                auth = tweepy.OAuthHandler( consumer_key, consumer_secret )
                auth.set_access_token( key, secret )
                self._api = tweepy.API( auth )
            
            else:
                logging.warning( error )
        return self._api

    def tweet( self, status ):
        this_api = self.api()
        if this_api is not None:
            this_api.update_status( status )
                