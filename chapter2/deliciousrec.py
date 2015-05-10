from pydelicious import get_popular, get_userposts, get_urlposts
import time

def initUserDict(tag):
    user_dict = { }
    popular_links = [ 
                    #u'http://coursera.org/',
                    u'http://ibm.com/',]
    for url in popular_links:
        # The get_urlposts API returns last 30 people who post the link
        while (True):
            try: 
                posts = get_urlposts(url)
                print 'fetch {0} users from {1}.'.format(len(posts), url)
                break
            except:
                print 'Error on {0}, retrying'.format(url)
                time.sleep(4)

        for post in posts:
            user = post['user']
            if user.strip() != '':
                user_dict[user] = { }
        print url
    return user_dict


def fillItems(user_dict):
    all_items = { }
    for user in user_dict:
        while (True):
            try:
                posts = get_userposts(user)
                break
            except:
                print 'Failed user' + user + ', retrying'
                time.sleep(4)

        for post in posts:
            url = post['url']
            user_dict[user][url] = 1.0
            all_items[url] = 1
        
    for ratings in user_dict.values():
        for item in all_items():
            if item not in ratings:
                ratings[item] = 0.0
