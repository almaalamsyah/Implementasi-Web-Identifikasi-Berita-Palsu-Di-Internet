
from newspaper import Article
from newsapi.newsapi_client import NewsApiClient
from model import predict

newsClient=NewsApiClient(api_key='83b920c473da4bfa91c8943cacb9f22d')
news_feed = newsClient.get_top_headlines( language='en',page_size=80)

def getArticlePredict(url):
    article = downloadArticle(url)
    result = predict(article.text)
    return {'url':url,
            'title':article.title,
            'text':article.text,
            'image':article.top_image,
            'pred_result':result[0],
            'pred_score':result[1]}

def downloadArticle(url):
    article=Article(url)
    article.download()
    article.parse()
    return article

def getSpecifArticle(currentReal=0,currentFake=0, index=0, maxReal=0,maxFake=0):
    global news_feed
    for i in range(index, len(news_feed['articles'])):
        # print(f"$%$%$$$%$% >>>>> {i}")
        article = news_feed['articles'][i]
        try:
            result = predict(downloadArticle(article['url']).text)
        except:
            continue
        article['pred_result']= result[0]
        article['pred_score']= result[1]
        article['date'] = article['publishedAt'][0:10]
        print(i,len(news_feed), index, currentReal ,article['title'][:10])

        if maxReal == 0 and maxFake ==0:
            return article, 0,0, i+1

        if article['pred_result'].upper() == "FAKE" and currentFake < maxFake:
            return article, currentReal,currentFake+1, i+1
        elif article['pred_result'].upper() == "REAL" and currentReal < maxReal:
            return article, currentReal+1,currentFake, i+1
    else:
        article = news_feed['articles'][0]
        # print(len(news_feed), index, currentReal )
        result = predict(downloadArticle(article['url']).text)
        article['pred_result']= result[0]
        article['pred_score']= result[1]
        article['date'] = article['publishedAt'][0:10]
        return article, currentReal,currentFake, 20