from configuration.imdb_client import get_imdb_service


def get_webpage_service(genre: str, iteration: int):
    client_imdb = get_imdb_service()
    url = "http://www.imdb.com/search/title?at=0&genres=" + genre + "&sort=moviemeter,asc&start=" + str(
        iteration * 50 + 1) + "&title_type=feature"

    try:
        c = client_imdb.request(url=url, method='GET')
        return c

    except Exception as e:
        print("error is ", e)
        print("could not open url", url)
