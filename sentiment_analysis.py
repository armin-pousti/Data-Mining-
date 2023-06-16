# Dmitrii Vlasov, Armin Pousti
from nltk.sentiment import SentimentIntensityAnalyzer
import csv

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    return compound_score

video_data = 'video_data.csv'
csv_output_file_path = 'video_data_with_sentiment.csv'

csv_file = open(video_data, 'r', newline='', encoding='utf-8')
reader = csv.DictReader(csv_file)
fieldnames = reader.fieldnames + ['sentiment_score']

output_file = open(csv_output_file_path, 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(output_file, fieldnames=fieldnames)
writer.writeheader()

for row in reader:
    title = row['title']
    comments = row['comments']
    sentiment_score = analyze_sentiment(comments)
    row['sentiment_score'] = sentiment_score
    # check if comments exist/are enabled
    if comments:
        sentiment_score = analyze_sentiment(comments)
    else:
        sentiment_score = "No comments to analyze"
    writer.writerow(row)
    print("Title:", title)
    print("Sentiment Score:", sentiment_score)
    print()

csv_file.close()
output_file.close()




##############################################EXAMPLE_FOR_REPORT########################################################
# text_neg = "The movie was an agonizing torture of incoherent storytelling and mind-numbingly dull characters. " \
#        "I would rather endure a root canal without anesthesia than suffer through that cinematic abomination again."
# text_pos = "This movie is pure cinematic magic, an unforgettable masterpiece that redefines the very essence " \
#            "of cinema itself."
# text_neu = "The movie was okay, neither particularly exciting nor overly disappointing. " \
#            "It was just average and didn't leave a lasting impression."
# sentiment_analysis_neg = analyze_sentiment(text_neg)
# print(sentiment_analysis_neg)
# sentiment_analysis_pos= analyze_sentiment(text_pos)
# print(sentiment_analysis_pos)
# sentiment_analysis_neu = analyze_sentiment(text_neu)
# print(sentiment_analysis_neu)