from stream_framework.feed_managers.base import Manager
from stream_framework.feed_managers.base import FanoutPriority
from core.models import Follow
from core.pin_feed import (
    AggregatedPinFeed, 
    PinFeed,
    UserPinFeed,
    NotificationPinFeed
)


class PinManager(Manager):
    # this example has both a normal feed and an aggregated feed (more like
    # how facebook or wanelo uses feeds)
    feed_classes = dict(
        normal=PinFeed,
        aggregated=AggregatedPinFeed,
        notification=NotificationPinFeed
    )
    user_feed_class = UserPinFeed

    def add_pin(self, pin):
        activity = pin.create_activity()
        # add user activity adds it to the user feed, and starts the fanout
        self.add_user_activity(pin.user_id, activity)

    def remove_pin(self, pin):
        activity = pin.create_activity()
        # removes the pin from the user's followers feeds
        self.remove_user_activity(pin.user_id, activity)

    def get_user_follower_ids(self, user_id):
        ids = Follow.objects.filter(target=user_id).values_list('user_id', flat=True)
        return {FanoutPriority.HIGH: ids}
    
    def mark_pins_seen(self, user_id, activity_ids):
        if not isinstance(activity_ids, (tuple, list)):
            activity_ids = [activity_ids]
        notification_obj = self.feed_classes['notification'](user_id)
        notification_obj.mark_activities(activity_ids)
    
    def mark_all_pins_seen(self, user_id):
        self.feed_classes['notification'](user_id).mark_all()

    def get_unseen_activities(self, user_id):
        activities = []
        count = self.count_unseen_pins(user_id=user_id)
        notification_feed = self.feed_classes['notification'](user_id)
        for notification in notification_feed[:count]:
            activities.extend(notification.last_activities)
        return activities

    def count_unseen_pins(self, user_id):
        return self.feed_classes['notification'](
            user_id).count_unseen()

    def count_unread_pins(self, user_id):
        return self.feed_classes['notification'](
            user_id).count_unread()


manager = PinManager()
