from stream_framework.aggregators.base import BaseAggregator


class NotificationAggregator(BaseAggregator):
    '''
    Aggregates based on the same verb and same time period
    '''

    def get_group(self, activity):
        '''
        Returns a group based on the day and verb
        '''
        verb = activity.verb.id
        date = activity.time.now()
        group = '%s-%s' % (verb, date)
        return group
    
    def rank(self, aggregated_activities):
        # just for testing
        aggregated_activities.sort(reverse=True)
        return aggregated_activities
