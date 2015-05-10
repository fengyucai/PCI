from deliciousrec import *

if __name__ == '__main__':
    delusers = initUserDict('programming')
    print 'Fetch {0} users.'.format(len(delusers))
    for user in delusers.keys():
        print user
    fillItems(delusers)
    for user in delusers.keys():
        print user
