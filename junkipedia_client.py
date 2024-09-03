import requests
import urllib.parse

class JunkipediaClient:
    BASE_URL = "https://www.junkipedia.org/api/v1/"

    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_posts_by_list(self, lists=None, post_types=["video" "photo" "link" "status"],  results_per_page=10, page_num=1):
        #Use the api_key in the request as a bearer token in the Authorization header
        lists_str = ','.join(map(str, lists))
        response = requests.get(f"{self.BASE_URL}?lists={lists_str}&per_page={results_per_page}&page={page_num}", headers={"Authorization": f"Bearer {self.api_key}"})

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    
    def fetch_all_posts_by_list(self, lists=None, results_per_page=10):
        all_posts = []
        page_num = 1
        while True:
            posts = self.fetch_posts_by_list(lists=lists, results_per_page=results_per_page, page_num=page_num)
            all_posts.extend(posts)
            if len(posts) < results_per_page or posts['links']['next'] is None:
                break
            page_num += 1
        return all_posts
    
    def fetch_posts_by_list_until_datetime(self, target_datetime='', lists=None, results_per_page=10):
        all_posts = []
        page_num = 1
        while True:
            posts = self.fetch_posts_by_list(lists, results_per_page=100, page_num=page_num)
            last_post = posts['data'][-1]
            if last_post['attributes']['published_at'] < '2021-01-01':
                break

            all_posts.extend(posts)

            page_num += 1
        
        return all_posts
    
    def fetch_posts_by_params(self, 
                              list_id = None, 
                              keyword="",
                              simple_query=False,
                           post_types=["video", "photo", "link", "status"],  
                           platform_names=["Bitchute","Facebook","GETTR","Gab","Instagram","OK","Parler","Podcast","Rumble","Telegram","TikTok","TruthSocial","Twitter","VK","YouTube"],
                           engagement_range = [0, 2147483646],
                           published_range = [0, 2147483646],
                           language_codes = [],
                           exclude=[],
                           results_per_page=10, 
                           channel_properties={},
                           person_properties={},
                           page_num=1):
        if list_id is None:
            query_string = f"{self.BASE_URL}posts?per_page={results_per_page}&page={page_num}"
        else:            
            query_string = f"{self.BASE_URL}lists/{list_id}/get_posts?per_page={results_per_page}&page={page_num}"

        if keyword is not None and len(keyword) > 0:
            #url encode the keyword
            keyword = urllib.parse.quote(keyword)
            query_string += f"&keyword={keyword}"
        if simple_query:
            query_string += "&simple_search=true"

        if engagement_range is not [0, 2147483646]:
            if engagement_range[0] is not None and engagement_range[0] > 0:
                query_string += f"&engagement_from={engagement_range[0]}.00"
            if engagement_range[1] is not None and engagement_range[1] < 2147483646:
                query_string += f"&engagement_to={engagement_range[1]}.00"
        
        if published_range is not [0, 2147483646]:
            if published_range[0] is not None and published_range[0] > 0:
                query_string += f"&published_at_from={published_range[0]}"
            if published_range[1] is not None and published_range[1] < 2147483646:
                query_string += f"&published_at_to={published_range[1]}"
        

        for post_type in post_types:
            query_string += f"&post_types[]={post_type}"

        for platform_name in platform_names:
            query_string += f"&platform_names[]={platform_name}"
        
        for language_code in language_codes:
            if language_code is not None and len(language_code) == 2:
                query_string += f"&language_codes[]={language_code.upper()}"
        
        for exclude_item in exclude:
            if exclude_item in ['replies', 'ads', 'posts']:
                query_string += f"&exclude[]={exclude_item}"
        
        for c_key, c_value in channel_properties.items():
            query_string += f"&channel[{c_key}]={c_value}"

        for p_key, p_value in person_properties.items():
            query_string += f"&person[{p_key}]={p_value}"

        response = requests.get(query_string, headers={"Authorization": f"Bearer {self.api_key}"})

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    # Seems to be a bug in the API, returns 503
    def fetch_posts_by_channel_id(self, channel_id, results_per_page=10, page_num=1):
        response = requests.get(f"{self.BASE_URL}channels/{channel_id}/get_posts", headers={"Authorization": f"Bearer {self.api_key}"})
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def search_channels(self, handle=None, search_term=None, channel_id=None, platform_id=[], platform_name=[], results_per_page=10, page_num=1):
        query_string = f"{self.BASE_URL}channels/search?per_page={results_per_page}&page={page_num}"
        if channel_id is not None:
            query_string += f"&channel_uid={channel_id}"
        if search_term is not None:
            query_string += f"&term={search_term}"
        if handle is not None:
            query_string += f"&handle={handle}"
        if len(platform_name) > 0:
            query_string += f"&platform_name={platform_name}"
        if len(platform_id) > 0:
            query_string += f"&platform_id={platform_id}"
                                                                                                
        response = requests.get(query_string, headers={"Authorization": f"Bearer {self.api_key}"})
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

if __name__ == "__main__":
    client = JunkipediaClient('pLHyu6LmcziyjgUAuoeTPTJw')
    for i in range(2):

        # posts = client.fetch_posts_by_params(list_id=7813, results_per_page=10, page_num=i+1)
        # print(posts)

        posts = client.fetch_posts_by_params(keyword="Trump", results_per_page=10, page_num=i+1)
        print(posts)

        # print("Channel ID", 10320346)
        # # posts = client.fetch_posts_by_channel_id(10320346, results_per_page=10, page_num=i+1)
        # print(posts)

    # channel = client.search_channels(channel_id=7187516)
    # print(channel)
    # posts = client.fetch_posts_by_channel_id(7187516, results_per_page=10, page_num=1)
    # print(posts)