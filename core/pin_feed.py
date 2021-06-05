from stream_framework.aggregators.base import RecentVerbAggregator
from stream_framework.feeds.redis import RedisFeed
from stream_framework.feeds.aggregated_feed.redis import RedisAggregatedFeed
# from stream_framework.feeds.aggregated_feed.notification_feed import RedisNotificationFeed
from stream_framework.feeds.notification_feed.redis import RedisNotificationFeed
from core.notification import NotificationAggregator


class PinFeed(RedisFeed):
    key_format = 'feed:normal:%(user_id)s'


class AggregatedPinFeed(RedisAggregatedFeed):
    key_format = 'feed:aggregated:%(user_id)s'
    aggregator_class = RecentVerbAggregator
    

class UserPinFeed(PinFeed):
    key_format = 'feed:user:%(user_id)s'


class NotificationPinFeed(RedisNotificationFeed):
    # : they key format determines where the data gets stored
    key_format = 'feed:notification:%(user_id)s'
    # : the aggregator controls how the activities get aggregated
    aggregator_class = NotificationAggregator
