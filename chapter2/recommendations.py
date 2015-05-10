# A dictionary of movie critics and their ratings of a small
# set of movies
critics = {'Lisa Rose' : {'Lady in the Water' : 2.5, 'Snakes on a Plane' : 3.5,
    'Just My Luck' : 3.0, 'Superman Returns' : 3.5, 'You, Me and Dupree' : 2.5,
    'The Night Listener' : 3.0},
    'Gene Seymour' : {'Lady in the Water' : 3.0, 'Snakes on a Plane' : 3.5,
    'Just My Luck' : 1.5, 'Superman Returns' : 5.0, 'The Night Listener' : 3.0,
    'You, Me and Dupree' : 3.5},
    'Micheal Phillips' : {'Lady in the Water' : 2.5, 'Snakes on a Plane' : 3.0,
    'Superman Returns' : 3.5, 'The Night Listener' : 4.0},
    'Claudia Puig' : {'Snakes on a Plane' : 3.5, 'Just My Luck' : 3.0,
    'The Night Listener' : 4.5, 'Superman Returns' : 4.0,
    'You, Me and Dupree' : 2.5},
    'Mick LaSalle' : {'Lady in the Water' : 3.0, 'Snakes on a Plane' : 4.0,
    'Just My Luck' : 2.0, 'Superman Returns' : 3.0, 'The Night Listener' : 3.0,
    'You, Me and Dupree' : 2.0},
    'Jack Matthews' : {'Lady in the Water' : 3.0, 'Snakes on a Plane' : 4.0,
    'The Night Listener' : 3.0, 'Superman Returns' : 5.0, 'You, Me and Dupree' : 3.5},
    'Toby' : {'Snakes on a Plane' : 4.5, 'You, Me and Dupree' : 1.0, 'Superman Returns' : 4.0}}


from math import sqrt

def sim_distance(prefs, person1, person2):
    # Get the list of shared items
    si = { }
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    if len(si) == 0: return 0
    # Add up squares of all the differences
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                        for item in si])
    return 1 / sqrt(1 + (sum_of_squares))


def max_sim_distance(prefs):
    l = len(prefs)
    persons = [item for item in prefs]
    max_sim = 0 
    pair = ['', '']
    for i in range(0, l):
        for j in range(i+1, l):
            curr_sim = sim_distance(prefs, persons[i], persons[j])
            if curr_sim > max_sim:
                max_sim = curr_sim
                pair[0] = persons[i]
                pair[1] = persons[j] 

    return (max_sim, pair[0], pair[1]) 

def sim_pearson(prefs, p1, p2):
    si = { } 
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    n = len(si)
    if n == 0: return 0
    
    sumx = sum([prefs[p1][item] for item in si])
    sumy = sum([prefs[p2][item] for item in si])
    sumx_sq = sum([pow(prefs[p1][item], 2) for item in si])
    sumy_sq = sum([pow(prefs[p2][item], 2) for item in si])
    sum_xy = sum([prefs[p1][item] * prefs[p2][item] for item in si])
    
    num = sum_xy - (sumx*sumy)/n
    den = sqrt((sumx_sq - pow(sumx, 2)/n) * (sumy_sq - pow(sumy, 2)/n))
    if den == 0: return 0
    
    return num / den

# Returns the best matches for a given person from the prefs dictionary
# Number of results and similarity function are optional params
def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other) 
            for other in prefs if other != person]
    # Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[0:n]

# Problem solved: What is your expected ratings of movies you haven't seen?
# answer: It is the average ratings of movies you haven't seen by people similar to you
# Get recommendation for a user by using a similarity-weighted average
# of every other user's rating
def getRecommendations(prefs, person, similarity=sim_pearson):
    totals = { }
    sim_sums = { }
    for other in prefs:
        if other != person:
            sim = similarity(prefs, person, other)
            if sim > 0:
                for item in prefs[other]:
                    if item not in prefs[person]:
                        totals.setdefault(item, 0)
                        totals[item] += prefs[other][item]*sim
                        sim_sums.setdefault(item, 0)
                        sim_sums[item] += sim

    rankings = [(total/sim_sums[item], item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings

# Flip item and person to get a data set
# for determing similarity between items
def transformPrefs(prefs):
    result = { }
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, { })
            result[item][person] = prefs[person][item]
    return result

def calculateSimilarItems(prefs, n=10):
    result = { }
    # Invert the preference matrix to be item-centric
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        c += 1
        if c % 100 == 0: print '%d / %d' % (c, len(itemPrefs))
        # Find the most similar n items for this one
        result[item] = topMatches(itemPrefs, item, n=n, similarity=sim_distance)
    return result

def getRecommendedItems(prefs, itemsMatch, user):
    user_ratings = prefs[user]
    scores = { }
    totalSim = { }
    for item, rating in user_ratings.items():
        for sim, item2 in itemsMatch[item]:
            if item2 not in user_ratings:
                scores.setdefault(item2, 0)
                scores[item2] += sim * rating
                totalSim.setdefault(item2, 0)
                totalSim[item2] += sim
    
    result = [(score/totalSim[item], item) for item, score in scores.items()]
    result.sort()
    result.reverse()
    return result


def loadMovieLens(path='data/movielens'):
    # Get movie titles
    movies = { }
    for line in open(path+'/u.item'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title
    # build dataset 
    prefs = { }
    for line in open(path+'/u.data'):
        (user, movieid, rating, ts) = line.split('\t')[0:4]
        prefs.setdefault(user, { })
        prefs[user][movies[movieid]] = float(rating)
    return prefs
    return result
