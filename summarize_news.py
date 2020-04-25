import newsProvider
import summarizer

if __name__ == '__main__':
    newsProvider = newsProvider.NewsProvider("Apple stock", 5)
    news = newsProvider.getNews()

    summary = {}
    for source, text in news.items():
        summarize = summarizer.Summarizer(text, source,5)
        print(source, summarize.summarize())
