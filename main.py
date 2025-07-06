from itertools import islice
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR
import json
import re

def fetch_comment(url=None, sort_by=SORT_BY_POPULAR, max_comments=10):
    output = {}
    downloader = YoutubeCommentDownloader()
    comments = downloader.get_comments_from_url(url, sort_by=sort_by)
    counter = 1
    for comment in islice(comments, max_comments):
        clean_text = clean_comment(comment.get("text"))
        output[str(counter)] = {
                "author": comment.get("author"),
                "text": clean_text,
                "likes": comment.get("votes"),
                "time": comment.get("time")
            }
        counter += 1
    return output

def clean_comment(text):
    # 1. Remove emojis (basic regex-based filtering)
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # Emoticons
                               u"\U0001F300-\U0001F5FF"  # Symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # Transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # Flags
                               u"\U00002500-\U00002BEF"  # Chinese characters
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)

    # 2. Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)

    # 3. Remove special characters except letters and numbers
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)

    # 4. Normalize whitespace and lowercase
    text = text.lower().strip()

    # 5. Remove repeated characters (e.g., "soooo" → "soo")
    text = re.sub(r'(.)\1{2,}', r'\1\1', text)

    # 6. Remove spammy short texts
    if len(text) < 5:
        return None

    return text
    
def write_to_file(data, filename='comments.json'):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

if __name__ == "__main__":
    try:
        # url = input("Enter the YouTube video URL: ")
        url = "https://www.youtube.com/watch?v=3MKZMOCCEuI"
        sort_by = SORT_BY_POPULAR  # or SORT_BY_NEWEST, SORT_BY_OLDEST
        max_comments = 2  # Set the maximum number of comments to retrieve
        if url:
            data = fetch_comment(url, sort_by, max_comments)
            print(json.dumps(data, indent=2))  # Use json.dumps to ensure proper JSON formatting
            write_to_file(data)
        else:
            print("No URL provided. Exiting.")
    except Exception as e:
        print(f"An error occurred: {e}")