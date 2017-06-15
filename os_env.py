import os

fname = 'windeployqt.exe'
for ifolder in os.environ.iteritems():
    try:
        files = os.listdir(ifolder[1])
        if fname in files:
            print ifolder[0]
    except:
        pass