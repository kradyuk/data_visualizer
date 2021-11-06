
count = 10

def myfunc(): 
#    global count
    count = count + 1
    print(count)
  
myfunc()


count = 10

def myfunc_fixed():
    global count
    count = count + 1
    print(count)
  
myfunc_fixed()

