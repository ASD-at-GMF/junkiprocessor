import pandas as pd
import json
import uuid

class DataHandler:
    
    @staticmethod
    def process_data(data):
        # Assuming 'data' is a list of dictionaries
        if not data:
            return pd.DataFrame()
        if 'data' in data:
            data = data['data']
        return data

    @staticmethod
    def save_to_csv(data, filename):
        df = pd.json_normalize(data)
        df.to_csv(filename, index=False)
    
    @staticmethod
    def save_to_excel(data, filename):
        df = pd.json_normalize(data)
        df.to_excel(filename)

    @staticmethod
    def save_to_json(data, filename):
        json_object = json.dumps(data, indent=4)
        
        # Writing to sample.json
        with open(filename, "w") as outfile:
            outfile.write(json_object)
            

    @staticmethod
    def save_to_parquet(data, filename):
        df = pd.json_normalize(data)
        df.to_parquet(filename)
    
    @staticmethod
    def save_to_pickle(data, filename):
        df = pd.json_normalize(data)
        df.to_pickle(filename)
    
    @staticmethod
    def save_to_sql(data):
        df = pd.json_normalize(data)
        df.to_sql(filename)
    
    @staticmethod
    def save_to_hdf(data, filename):
        df = pd.json_normalize(data)
        df.to_hdf(filename)
    
    @staticmethod
    def save_to_feather(data, filename):
        df = pd.json_normalize(data)
        df.to_feather(filename)
    
    @staticmethod
    def save_to_stata(data, filename):
        df = pd.json_normalize(data)
        df.to_stata(filename)
    
    @staticmethod
    def save_to_msgpack(data, filename):
        df = pd.json_normalize(data)
        df.to_msgpack(filename)
    
    @staticmethod
    def save_to_gbq(data, filename):
        df = pd.json_normalize(data)
        df.to_gbq(filename)
    
    @staticmethod
    def save_to_html(data, filename):
        df = pd.json_normalize(data)
        df.to_html(filename)
    
    @staticmethod
    def save_to_latex(data, filename):
        df = pd.json_normalize(data)
        df.to_latex(filename)
    
    @staticmethod
    def save_to_clipboard(data):
        df = pd.json_normalize(data)
        df.to_clipboard()
    
    @staticmethod
    def save_to_markdown(data, filename):
        df = pd.json_normalize(data)
        df.to_markdown(filename)
    
    @staticmethod
    def to_string(data):
        return json.dumps(data)
    
    @staticmethod
    def to_dict():
        return data
    
    @staticmethod
    def to_numpy(data):
        df = pd.json_normalize(data)
        return df.to_numpy()
    
    @staticmethod
    def to_records(data):
        df = pd.json_normalize(data)
        return df.to_records()
    
    @staticmethod
    def to_opencti(posts):
        opencti_objects = []

        for post in posts:
            post_attributes = post['attributes']

            # Create the main post object
            post_object = {
                "id": f"stix-object--{str(uuid.uuid4())}",
                "type": "x-opencti-social-media-post",
                "created": post_attributes['created_at'],
                "modified": post_attributes['updated_at'],
                "created_by_ref": f"stix-object--{str(uuid.uuid4())}",
                "x_opencti_created": post_attributes['created_at'],
                "x_opencti_modified": post_attributes['updated_at'],
                "x_opencti_description": post_attributes.get('complete_post_text', ''),
                "x_opencti_external_id": post_attributes['id'],
                "x_opencti_url": post_attributes['url'],
                "x_opencti_date": post_attributes['published_at'],
                "x_opencti_source": "Junkipedia",
                "x_opencti_author_identity": post_attributes['channel_id'],
                "x_opencti_channel": post_attributes['channel_id'],
                "x_opencti_social_media_platform": post_attributes['search_data_fields']['platform_name'],
                "x_opencti_like_count": post_attributes['engagement_fields']['likes_count'],
                "x_opencti_comment_count": post_attributes['engagement_fields']['comments_count'],
                "x_opencti_share_count": post_attributes['engagement_fields']['shares_count'],
                "x_opencti_view_count": post_attributes['engagement_fields']['views_count'],
            }
            opencti_objects.append(post_object)

            # Create the channel object
            channel = post['channel']
            channel_object = {
                "id": f"stix-object--{str(uuid.uuid4())}",
                "type": "x-opencti-organization",
                "created": channel['created_at'],
                "modified": channel['updated_at'],
                "name": channel['channel_name'],
                "identity_class": "organization",
                "x_opencti_aliases": [channel['channel_name'], channel['channel_uid']],
                "x_opencti_external_id": channel['id'],
                "x_opencti_platform": post_attributes['search_data_fields']['platform_name'],
                "x_opencti_url": channel['channel_data']['url']
            }
            opencti_objects.append(channel_object)

            # Link the post to the channel
            relationship_object = {
                "id": f"stix-object--{str(uuid.uuid4())}",
                "type": "relationship",
                "relationship_type": "belongs-to",
                "source_ref": post_object['id'],
                "target_ref": channel_object['id'],
                "start_time": post_attributes['created_at'],
                "stop_time": post_attributes['updated_at']
            }
            opencti_objects.append(relationship_object)

            # Create media objects if any
            for media in post_attributes['post_data']['entities']['media']:
                media_object = {
                    "id": f"stix-object--{str(uuid.uuid4())}",
                    "type": f"x-opencti-media-{media['type']}",
                    "created": post_attributes['created_at'],
                    "modified": post_attributes['updated_at'],
                    "url": media['media_url_https'],
                    "x_opencti_media_type": media['type'],
                    "x_opencti_display_url": media['display_url'],
                    "x_opencti_expanded_url": media['expanded_url'],
                    "x_opencti_external_id": media['id_str'],
                    "x_opencti_description": media.get('description', '')
                }
                opencti_objects.append(media_object)

                # Link the media to the post
                media_relationship_object = {
                    "id": f"stix-object--{str(uuid.uuid4())}",
                    "type": "relationship",
                    "relationship_type": "contains",
                    "source_ref": post_object['id'],
                    "target_ref": media_object['id'],
                    "start_time": post_attributes['created_at'],
                    "stop_time": post_attributes['updated_at']
                }
                opencti_objects.append(media_relationship_object)

        return opencti_objects
    
    @staticmethod
    def save_to_opencti(posts, filename):
        opencti_objects = DataHandler.to_opencti(posts)
        with open(filename, 'w') as f:
            json.dump(opencti_objects, f, indent=4)
    

if __name__ == "__main__":
    data = [{"id": 1, "title": "Post 1"}, {"id": 2, "title": "Post 2"}]
    handler = DataHandler()
    df = handler.process_data(data)
    handler.save_to_csv(df, "posts.csv")
    print(df)