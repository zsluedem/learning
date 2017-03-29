class mathrow():
    def __init__(self, row, allnum=False):
        if allnum:
            self.data = [float(row[i]) for i in range(len(row) - 1)]
        else:
            self.data = row[0:len(row) - 1]
        self.match = int(row[len(row)-1])


def loadmatch(f, allnum=False):
    rows = []
    for line in file(f):
        rows.append(mathrow(line.split(','), allnum))
    return rows


def lineartrain(rows):
    averages = {}
    counts = {}

    for row in rows:
        cl = row.match

        averages.setdefault(cl, [0.0] *(len(row.data)))
        counts.setdefault(cl, 0)

        for i in range(len(row.data)):
            averages[cl][i] += float(row.data[i])

        counts[cl] += 1

    for cl, avg in averages.iteritems():
        for i in range(len(avg)):
            avg[i]/=counts[cl]

    return averages


def dotproduct(v1, v2):
    return sum([v1[i]*v2[i] for i in range(len(v1))])


def dpclassify(point, avgs):
    b = (dotproduct(avgs[1], avgs[1]) - dotproduct(avgs[0], avgs[0])) /2
    y = dotproduct(point, avgs[0]) - dotproduct(point, avgs[1]) +b
    if y >0:
        return 0
    else:
        return 1


def yesno(v):
    if v =='yes':
        return 1
    elif v == 'no':
        return -1
    else:
        return 0