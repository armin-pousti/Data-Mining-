# Dmitrii Vlasov, Armin Pousti
# NOTE: in order to run the following code line 8 needs to be modified using one's own YouTube API key
import csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# change the following using personal API key
api_key = 'YOUR API KEY'
youtube = build('youtube', 'v3', developerKey=api_key)

# searching for videos based on a specific topic/category
search_response = youtube.search().list(
    q='music in english',
    part='id',
    maxResults=50
).execute()

video_details = []

# process the first page of search results
for item in search_response['items']:
    video_id = item['id'].get('videoId')
    if video_id:
        video_response = youtube.videos().list(
            id=video_id,
            part='snippet,statistics'
        ).execute()
        video_details.append(video_response['items'][0])

# process subsequent pages of search results
page_count = 1

while 'nextPageToken' in search_response:
    next_page_token = search_response['nextPageToken']
    search_response = youtube.search().list(
        q='music in english',
        part='id',
        maxResults=50,
        pageToken=next_page_token
    ).execute()

    for item in search_response['items']:
        video_id = item['id'].get('videoId')
        if video_id:
            video_response = youtube.videos().list(
                id=video_id,
                part='snippet,statistics'
            ).execute()
            video_details.append(video_response['items'][0])

    page_count += 1

    # change this to change the number of pages  (50 videos per page)
    if page_count >= 3:
        break

# due to limitation of the API, an additional API request needs to be done individually for each video
for video in video_details:
    video_id = video['id']

    try:
        comments_response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=50
        ).execute()

        video['comments'] = []

        if 'items' in comments_response:
            for comment in comments_response['items']:
                comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                video['comments'].append(comment_text)


    except HttpError as e:

        if e.resp.status == 403 and b'commentsDisabled' in e.content:
            # vdeo has disabled comments
            video['comments'] = []

# Save the video details and comments in a CSV file
csv_file_path = 'video_data.csv'
fields = ['title', 'description', 'viewCount', 'likeCount', 'commentCount', 'publishedAt', 'comments']

csv_file = open(csv_file_path, 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(csv_file, fieldnames=fields)
writer.writeheader()
writer.writerows(
    {
        'title': item['snippet']['title'],
        'description': item['snippet']['description'],
        'viewCount': item['statistics']['viewCount'],
        'likeCount': item['statistics'].get('likeCount', 0),
        'commentCount': item['statistics'].get('commentCount', 0),
        'publishedAt': item['snippet']['publishedAt'],
        'comments': '\n'.join(item['comments']) if 'comments' in item else ''
    }
    for item in video_details
)
csv_file.close()
