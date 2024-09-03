from junkipedia_client import JunkipediaClient
from data_handler import DataHandler

def main():
    # Define the lists you want to fetch 8020-8040
    lists = [8034, 8035, 8036, 8037,8038, 8039, 8044, 8045, 8047, 8048, 8049, 8050, 8051, 8054, 8055, 8056]
    
    # Initialize the Junkipedia client
    client = JunkipediaClient('fakeApiKey')
    
    # Fetch posts
    posts = client.fetch_posts(lists, results_per_page=10)
    
    # Initialize the data handler
    handler = DataHandler()
    
    # Process the data
    df = handler.process_data(posts)
    
    # Save the data to a CSV file
    handler.save_to_csv(df, "junkipedia_posts_fb.csv")
    handler.save_to_excel(df, "junkipedia_posts_fb.xlsx")
    handler.save_to_json(df, "junkipedia_posts_fb.json")
    print("Data saved to junkipedia_posts.csv")

if __name__ == "__main__":
    main()