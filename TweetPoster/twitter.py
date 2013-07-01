from datetime import datetime

from requests_oauthlib import OAuth1

from TweetPoster import User, config


class Twitter(User):

    def __init__(self, *a, **kw):
        super(Twitter, self).__init__(*a, **kw)

        self.session.auth = OAuth1(
            config['twitter']['consumer_key'],
            config['twitter']['consumer_secret'],
            config['twitter']['access_token'],
            config['twitter']['access_secret'],
            signature_type='auth_header'
        )

    def get_tweet(self, tweet_id):
        url = 'https://api.twitter.com/1.1/statuses/show.json'
        params = {
            'id': tweet_id,
            'include_entities': 1,
        }

        r = self.get(url, params=params)
        assert r.status_code == 200, r.status_code

        return Tweet(r.json())


class Tweet(object):

    def __init__(self, json):
        self.user = TwitterUser(json['user'])
        self.text = json['text']
        self.id = json['id']
        self.in_reply_to = json['in_reply_to_status_id_str']
        self.entities = json['entities']
        self.link = 'https://twitter.com/{0}/status/{1}'.format(self.user.name, self.id)

        self.datetime = datetime.strptime(json['created_at'], '%a %b %d %H:%M:%S +0000 %Y')


class TwitterUser(object):

    def __init__(self, json):
        self.name = json['screen_name']
        self.link = 'https://twitter.com/' + self.name