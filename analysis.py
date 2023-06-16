# Dmitrii Vlasov, Armin Pousti
import pandas as pd
import matplotlib.pyplot as plt

video_data = pd.read_csv("video_data.csv")
# removing duplicates
video_data = video_data.drop_duplicates()

# converting the data to datetime type and sort by date
video_data['publishedAt'] = pd.to_datetime(video_data['publishedAt'])
video_data.sort_values(by='publishedAt', inplace=True)

average_view_count = video_data['viewCount'].mean()
average_like_count = video_data['likeCount'].mean()
average_comment_count = video_data['commentCount'].mean()

# finding the most viewed, liked, and commented videos
most_viewed_video = video_data.loc[video_data['viewCount'].idxmax()]
most_liked_video = video_data.loc[video_data['likeCount'].idxmax()]
most_disliked_video = video_data.loc[video_data['commentCount'].idxmax()]


# correlation between variables
correlation = video_data[['viewCount', 'likeCount', 'commentCount']].corr()
print(correlation)

# creating a figure and three subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10))

# plotting the view count
video_data.plot(x='publishedAt', y='viewCount', kind='line', ax=ax1)
ax1.set_ylabel('View Count')

# plotting the like count
video_data.plot(x='publishedAt', y='likeCount', kind='line', ax=ax2)
ax2.set_ylabel('Like Count')

# plotting the comment count
video_data.plot(x='publishedAt', y='commentCount', kind='line', ax=ax3)
ax3.set_ylabel('Comment Count')

plt.xlabel('Published Date')
plt.suptitle('Video Metrics Over Time')

# may be modified to change the number of labeled peaks on graphs
n_labels = 6
label_fontsize = 8

# labels for view count peaks
view_peaks = video_data[['publishedAt', 'viewCount']].copy()
view_peaks['title'] = video_data['title']
view_peaks = view_peaks.loc[view_peaks.groupby('title')['viewCount'].idxmax()]
view_peaks = view_peaks.nlargest(n_labels, 'viewCount')
for _, row in view_peaks.iterrows():
    ax1.annotate(row['title'], xy=(row['publishedAt'], row['viewCount']),
                 xytext=(5, 5), textcoords='offset points', color='red', fontsize=label_fontsize)

# labels for like count peaks
like_peaks = video_data[['publishedAt', 'likeCount']].copy()
like_peaks['title'] = video_data['title']
like_peaks = like_peaks.loc[like_peaks.groupby('title')['likeCount'].idxmax()]
like_peaks = like_peaks.nlargest(n_labels, 'likeCount')
for _, row in like_peaks.iterrows():
    ax2.annotate(row['title'], xy=(row['publishedAt'], row['likeCount']),
                 xytext=(5, 5), textcoords='offset points', color='red', fontsize=label_fontsize)

# labels for comment count peaks
comment_peaks = video_data[['publishedAt', 'commentCount']].copy()
comment_peaks['title'] = video_data['title']
comment_peaks = comment_peaks.loc[comment_peaks.groupby('title')['commentCount'].idxmax()]
comment_peaks = comment_peaks.nlargest(n_labels, 'commentCount')
for _, row in comment_peaks.iterrows():
    ax3.annotate(row['title'], xy=(row['publishedAt'], row['commentCount']),
                 xytext=(5, 5), textcoords='offset points', color='red', fontsize=label_fontsize)
plt.tight_layout()
plt.show()