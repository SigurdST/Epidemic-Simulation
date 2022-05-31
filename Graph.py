def text(x,y): # To open a file in write mode, and write the lenght of the list
    f = open(y, "a")
    f.write(str(len(x)) + ",")
    f.close()
def mean(x,y): # To open a file in write mode, and write the mean of the values in a list
    f = open(y, "a")
    if len(x)>0:
        f.write(str(sum(x)/len(x)) + ",")
    else:
        f.write(str(0))
    f.close()
def list(y): # To convert the text in a list of float
    with open(y, "r") as tf:
        l = tf.read().split(',')
    del l[-1]
    l1 = [float(i) for i in l]
    return l1