import pickle

from pytrends.request import TrendReq


def save_obj(obj, name):
    with open(name + '.pkl', 'ab') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq()

# Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
pytrend.build_payload(kw_list=['fashion', 'trend'])

# Interest Over Time
interest_over_time_df = pytrend.interest_over_time()
save_obj(interest_over_time_df, 'time_interest')

# Interest by Region
interest_by_region_df = pytrend.interest_by_region()
save_obj(interest_by_region_df, 'region_interest')

# Related Queries, returns a dictionary of dataframes
related_queries_dict = pytrend.related_queries()
save_obj(related_queries_dict, 'queries')

# Get Google Hot Trends data
trending_searches_df = pytrend.trending_searches()
save_obj(trending_searches_df, 'trending')

# Get Google Top Charts
top_charts_df = pytrend.top_charts(cid='fashion_labels', date=201712)
save_obj(top_charts_df, 'charts')

# Get Google Keyword Suggestions
suggestions_dict = pytrend.suggestions(keyword='fashion')
save_obj(suggestions_dict, 'keywords')
