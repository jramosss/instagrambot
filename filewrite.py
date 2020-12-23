import os

def write_to_file (listt,filename=None,username=None):
    fname = ""
    i = 1
    PY = '.py'
    if filename is None:
        if username is None:
            username = 'someone`s'

        fname = username + '_followers'
        while (os.path.isfile(fname+PY)):
            fname = username + '_followers' + str(i)
            i += 1

    else:
        fname = filename
        while (os.path.isfile(fname+PY)):
            fname = filename + i
            i += 1

    fname += PY
    f = open(fname,'x')
    
    f.write('followers = ')
    f.close()
    
    f = open(fname,'a')
    f.write(listt.__str__())
    f.close()
