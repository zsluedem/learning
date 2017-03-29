# coding = utf-8

critics={
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0},
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5},
    'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.0,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0},
    'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'The Night Listener': 4.5,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5},
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 2.0},
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'The Night Listener': 3.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5},
    'Toby': {
        'Snakes on a Plane':4.5,
        'You, Me and Dupree':1.0,
        'Superman Returns':4.0}
    }

from math import sqrt


def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    if len(si) == 0:
        return 0

    sum_of_suquare = sum([pow(prefs[person1][item]-prefs[person2][item], 2)
                          for item in prefs[person1] if item in prefs[person2]])

    return 1/(1+sqrt(sum_of_suquare))


def sim_pearson(prefs, p1, p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    n = len(si)

    if n == 0:
        return 1

    sum1 = sum([prefs[p1][i] for i in si])
    sum2 = sum([prefs[p2][i] for i in si])

    sum1Sq = sum([pow(prefs[p1][i], 2) for i in si])
    sum2Sq = sum([pow(prefs[p2][i], 2) for i in si])

    pSum = sum([prefs[p1][i] * prefs[p2][i] for i in si])

    num = pSum - (sum1 * sum2/n)
    den = sqrt((sum1Sq-pow(sum1, 2)/n) * (sum2Sq-pow(sum2, 2)/n))
    if den == 0:
        return 0
    r = num/den
    return r


def topMatches(prefs, person, similarity=sim_pearson):
    score = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    score.sort()
    score.reverse()
    return score


def getRecommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    simsums = {}

    for other in prefs:
        if other == person:
            continue
        sim = similarity(prefs, person, other)
        # print sim
        if sim < 0:
            continue
        for item in prefs[other]:
            # print item
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim

                simsums.setdefault(item, 0)
                simsums[item] += sim
                # print totals

    rankings = [(total/simsums[item], item) for item, total in totals.items()]

    rankings.sort()
    rankings.reverse()
    return rankings


def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            result[item][person] = prefs[person][item]
    return result


def calculateSimilarItem(prefs, n=10):
    resutl = {}

    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        c += 1
        if c % 100 == 0:
            print "%d / %d " % (c, len(itemPrefs))
        scores = topMatches(itemPrefs, item, similarity=sim_distance)
        resutl[item] = scores

    return resutl


def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}
    for (item , rating) in userRatings.items():
        for (similarity, item2) in itemMatch[item]:
            if item2 in userRatings:
                continue
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating

            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity

        rankings = [(score/totalSim[item], item) for item,score in scores.items()]
        rankings.sort()
        rankings.reverse()
        return rankings




if __name__ == "__main__":
    # print sim_distance(critics, 'Lisa Rose', 'Gene Seymour')
    # print sim_pearson(critics, 'Lisa Rose', 'Gene Seymour')
    # print topMatches(critics, "Lisa Rose")
    print getRecommendations(critics, "Toby")
    print calculateSimilarItem(critics)
