from itertools import islice
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR
import json

def main(url=None, sort_by=SORT_BY_POPULAR, max_comments=10):
    output = {}
    downloader = YoutubeCommentDownloader()
    comments = downloader.get_comments_from_url(url, sort_by=sort_by)
    counter = 1
    for comment in islice(comments, max_comments):
        output[str(counter)] = comment.get('text')  # Convert key to string
        counter += 1
    return output

def write_to_file(data, filename='comments.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)

if __name__ == "__main__":
    try:
        # url = input("Enter the YouTube video URL: ")
        url = "https://www.youtube.com/watch?v=3MKZMOCCEuI"
        sort_by = SORT_BY_POPULAR  # or SORT_BY_NEWEST, SORT_BY_OLDEST
        max_comments = 10  # Set the maximum number of comments to retrieve
        if url:
            data = main(url, sort_by, max_comments)
            print(json.dumps(data, indent=2))  # Use json.dumps to ensure proper JSON formatting
            write_to_file(data)
        else:
            print("No URL provided. Exiting.")
    except Exception as e:
        print(f"An error occurred: {e}")