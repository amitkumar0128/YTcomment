from itertools import islice
from youtube_comment_downloader import *
import json

def main(url=None):
    output = {}
    downloader = YoutubeCommentDownloader()
    comments = downloader.get_comments_from_url(url, sort_by=SORT_BY_POPULAR)
    i=1
    for comment in islice(comments, 10):
        output[str(i)] = comment  # Convert key to string
        i += 1
    return output

if __name__ == "__main__":
    url = input("Enter the YouTube video URL: ")
    if url:
        print(json.dumps(main(url)))  # Use json.dumps to ensure proper JSON formatting
    else:
        print("No URL provided. Exiting.")