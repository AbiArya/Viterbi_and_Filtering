import random
import pygame
import time
#a row will be the y, and the columns will be x. 2d arrays are [row][col] [y][x]
def generateMap(r):
    norm=5000
    highway=2000
    hard=2000
    blocked=1000
    #norm=50
    #highway=20
    #hard=20
    #blocked=10
    fileobj=open('map' + str(r) + '.txt', 'w')#change str(1) so it can make 100 unique files
    map=[]
    for a in range(100):#CHANGE 10 TO 100
        tmprow=[]
        b=0
        str1=''
        while(b<100):#CHANGE 10 TO 100
            num=random.randint(0,9)
            if(num<5):
                if(norm>0):
                    tmprow.append('n')
                    str1+='n'
                    norm=norm-1
                    b=b+1
            elif(num<7):
                if(highway>0):
                    tmprow.append('h')
                    str1+='h'
                    highway-=1
                    b+=1
            elif(num<9):
                if(hard>0):
                    tmprow.append('t')
                    str1+='t'
                    hard-=1
                    b+=1
            else:
                if(blocked>0):
                    tmprow.append('b')
                    str1+='b'
                    blocked-=1
                    b+=1
        map.append(tmprow)
        fileobj.write(str1+'\n')

    return map

def generateData(map1,y,u):
    currx=random.randint(0,99)#CHANGE 9 TO 99
    curry=random.randint(0,99)#CHANGE 9 TO 99
    fileobj = open('ground' + str(y) +str(u) + '.txt', 'w')  # change str(1) so it can make 100 unique files
    actions=''
    sensor=''
    while(map1[curry][currx]=='b'):
        currx = random.randint(0, 99)#CHANGE 9 TO 99
        curry = random.randint(0, 99)#CHANGE 9 TO 99
    fileobj.write(str(currx)+','+str(curry)+'\n')
    for i in range(100):
        actionnum=random.randint(0,3)#to randomize actions. 0 is left, 1 is right, 2 is up, 3 is down
        if(actionnum==0):
            actions+='l'
            willmove=random.randint(0,10)
            if(willmove<9 and currx!=0 and map1[curry][currx-1]!='b'):
                currx-=1
            fileobj.write(str(currx)+','+str(curry)+'\n')
        elif(actionnum==1):
            actions+='r'
            willmove=random.randint(0,10)
            if(willmove<9 and currx!=99 and map1[curry][currx+1]!='b'):#CHANGE 9 TO ANOTHER NUMBER, DEPENDING ON MAP SIZES
                currx+=1
            fileobj.write(str(currx)+','+str(curry)+'\n')
        elif(actionnum==2):
            actions+='u'
            willmove=random.randint(0,10)
            if(willmove<9 and curry!=0 and map1[curry-1][currx]!='b'):
                curry-=1
            fileobj.write(str(currx)+','+str(curry)+'\n')
        else:
            actions+='d'
            willmove=random.randint(0,10)
            if(willmove<9 and curry!=99 and map1[curry+1][currx]!='b'):#CHANGE 9 TO ANOTHER NUMBER, DEPENDING ON MAP SIZES
                curry+=1
            fileobj.write(str(currx)+','+str(curry)+'\n')
        willdetect=random.randint(0,10)
        if(map1[curry][currx]=='n'):
            if(willdetect<9):
                sensor+=map1[curry][currx]
            else:
                fail=random.randint(0,2)
                if(fail==0):
                    sensor+='h'
                else:
                    sensor+='t'
        elif(map1[curry][currx]=='t'):
            if (willdetect < 9):
                sensor += map1[curry][currx]
            else:
                fail = random.randint(0,2)
                if (fail == 0):
                    sensor += 'h'
                else:
                    sensor += 'n'
        else:
            if (willdetect < 9):
                sensor += map1[curry][currx]
            else:
                fail = random.randint(0,2)
                if (fail == 0):
                    sensor += 'n'
                else:
                    sensor += 't'
    fileobj.write(actions+'\n')
    fileobj.write(sensor)

def takeMap(num):
    fileobj=open('map'+str(num)+'.txt','r')#CHANGE THE 2 TO NUM
    map=[]
    for i in range(100):
        row=[]
        readln=fileobj.readline()
        for a in readln:
            if(a!='\n'):
                row.append(a)
        map.append(row)
    return map

def getLoc(b,count):
    fileobj=open('ground'+str(b)+'.txt','r')
    x=0
    y=0
    for i in range(count+2):
        num=fileobj.readline()
        x=num[0:num.index(',')]
        y=num[num.index(',')+1:len(num)-1]
    return str(x),str(y)

def dist(x1,y1,x2,y2):
    tmpx=(float(x1)-x2)**2
    tmpy=(float(y1)-y2)**2
    tot=(tmpx+tmpy)**(.5)
    return tot

def qsort(inlist):
    if inlist == []:
        return []
    else:
        pivot = inlist[0]
        lesser = qsort([x for x in inlist[1:] if x < pivot])
        greater = qsort([x for x in inlist[1:] if x >= pivot])
        return lesser + [pivot] + greater

def getmax(arr):
    xmax=0
    ymax=0
    max=0
    for i in range(100):
        for j in range(100):
            if(arr[i][j]>max):
                max=arr[i][j]
                xmax=j
                ymax=i
    return xmax,ymax,max

def getmax1(arr):
    xmax1=[]
    ymax1=[]
    max1=[]
    b = sorted(range(len(arr)), key=lambda x: arr[x])[-10:]
    for val in b:
        xmax1.append(val%100)
        ymax1.append(int(val/100))
    realxmax=b[9]%100
    realymax=int(b[9]/100)
    return xmax1,ymax1,realxmax,realymax

realans=[]
def getPath(count,xmax,ymax,realxmax,realymax,paths):
    ans = []
    tmp = count
    for num in range(10):
        tmp = count
        tmpans=[]
        xmax2=xmax[num]
        ymax2=ymax[num]
        for i in range(count):
            newx = paths[ymax2][xmax2][tmp][0]
            newy = paths[ymax2][xmax2][tmp][1]
            tmpans.append(paths[ymax2][xmax2][tmp])
            #print(paths[ymax][xmax][tmp])
            ymax2 = newy
            xmax2 = newx

            tmp -= 1
        ans.append(tmpans)
    realans=[]
    tmp=count
    ymax2=realymax
    xmax2=realxmax

    for i in range(count):
        newx = paths[ymax2][xmax2][tmp][0]
        newy = paths[ymax2][xmax2][tmp][1]
        realans.append(paths[ymax2][xmax2][tmp])
        # print(paths[ymax][xmax][tmp])
        ymax2 = newy
        xmax2 = newx

        tmp -= 1
    return ans, realans

def getData(abc):
    fileobj=open('ground'+str(abc)+'.txt','r')
    firstline = fileobj.readline()
    initX = firstline[0:firstline.index(',')]
    initY = firstline[firstline.index(',') + 1:len(firstline)-1]
    #initY = firstline[0:firstline.index(',')]
    #initX = firstline[firstline.index(',') + 1:len(firstline)-1]
    actions=''
    evidence=''
    for i, line in enumerate(fileobj):
        if i == 100:
            actions+=line
        elif i == 101:
            evidence+=line
    actions1=actions[0:100]
    evidence1=evidence[0:100]
    #print(actions1)
    #print(evidence1)
    #print(initX)
    #print(initY)
    return actions1,evidence1,initX,initY

'''
def filtering(actions,evidence,map,probgrid,count):#a row will be the y, and the columns will be x. 2d arrays are [row][col] [y][x]
    ev=evidence[count]
    act=actions[count]
    newgrid=[]
    if(act=='r'):
        for count1, y in enumerate(map):#iterates rows/y
            tmpgridrow=[]
            for count2, x in enumerate(y):#iterates cols/x
                if(map[count1][count2]!='b'):#makes sure the block is not blocked
                    if(count2==0):#when moving right, we know it'll only be at 0/the border if movement fails
                        tmpval=probgrid[count1][count2]
                        if (map[count1][count2 + 1] != 'b'):
                            v1 = .1
                        else:
                            v1 = 1
                        if(ev!=map[count1][count2]):
                            v2=.05
                        else:
                            v2=.9
                        tmpgridrow.append(tmpval*v1*v2)
                    else:# if the val is not at the left border
                        tmpval=probgrid[count1][count2]
                        if(ev!=map[count1][count2]):
                            v2=.05
                        else:
                            v2=.9
                        if(count2==99):
                            v1=1
                        else:
                            v1=.1
                        newval=tmpval*v1*v2
                        if(map[count1][count2-1]!='b'):
                            v3=probgrid[count1][count2-1]
                            stuff=v3*.9*v2
                            newval+=stuff
                        tmpgridrow.append(newval)
                else:
                    tmpgridrow.append(0)
            newgrid.append(tmpgridrow)
    elif(act=='l'):
        for count1, y in enumerate(map):#iterates rows/y
            tmpgridrow=[]
            for count2, x in enumerate(y):#iterates cols/x
                if(map[count1][count2]!='b'):
                    if(count2==99):
                        tmpval=probgrid[count1][count2]
                        if (map[count1][count2 - 1] != 'b'):
                            v1 = .1
                        else:
                            v1 = 1
                        if(ev!=map[count1][count2]):
                            v2=.05
                        else:
                            v2=.9
                        tmpgridrow.append(tmpval*v1*v2)
                    else:
                        tmpval=probgrid[count1][count2]
                        if(ev!=map[count1][count2]):
                            v2=.05
                        else:
                            v2=.9
                        if(count2==0):
                            v1=1
                        else:
                            v1=.1
                        newval=tmpval*v1*v2
                        if(map[count1][count2+1]!='b'):
                            v3=probgrid[count1][count2+1]
                            stuff=v3*.9*v2
                            newval+=stuff
                        tmpgridrow.append(newval)
                else:
                    tmpgridrow.append(0)
            newgrid.append(tmpgridrow)
    elif(act=='u'):
        for count1, y in enumerate(map):#iterates rows/y
            tmpgridrow=[]
            for count2, x in enumerate(y):#iterates cols/x
                if(map[count1][count2]!='b'):
                    if(count1==99):
                        tmpval=probgrid[count1][count2]
                        if (map[count1-1][count2] != 'b'):
                            v1 = .1
                        else:
                            v1 = 1
                        if(ev!=map[count1][count2]):
                            v2=.05
                        else:
                            v2=.9
                        tmpgridrow.append(tmpval*v1*v2)
                    else:
                        tmpval=probgrid[count1][count2]
                        if(ev!=map[count1][count2]):
                            v2=.05
                        else:
                            v2=.9
                        if(count1==0):
                            v1=1
                        else:
                            v1=.1
                        newval=tmpval*v1*v2
                        if(map[count1+1][count2]!='b'):
                            v3=probgrid[count1+1][count2]
                            stuff=v3*.9*v2
                            newval+=stuff
                        tmpgridrow.append(newval)
                else:
                    tmpgridrow.append(0)
            newgrid.append(tmpgridrow)
    else:
        for count1, y in enumerate(map):#iterates rows/y
            tmpgridrow=[]
            for count2, x in enumerate(y):#iterates cols/x
                if(map[count1][count2]!='b'):
                    if(count1==0):
                        tmpval=probgrid[count1][count2]
                        if (map[count1+1][count2] != 'b'):
                            v1 = .1
                        else:
                            v1 = 1
                        if(ev!=map[count1][count2]):
                            v2=.05
                        else:
                            v2=.9
                        tmpgridrow.append(tmpval*v1*v2)
                    else:
                        tmpval=probgrid[count1][count2]
                        if(ev!=map[count1][count2]):
                            v2=.05
                        else:
                            v2=.9
                        if(count1==99):
                            v1=1
                        else:
                            v1=.1
                        newval=tmpval*v1*v2
                        if(map[count1-1][count2]!='b'):
                            v3=probgrid[count1-1][count2]
                            stuff=v3*.9*v2
                            newval+=stuff
                        tmpgridrow.append(newval)
                else:
                    tmpgridrow.append(0)
            newgrid.append(tmpgridrow)
'''

avg=0

def runprog():
    distances=[]
    for i in range(10):
        tmpmap = takeMap(i)
        for q in range(10):
            print(q)
            curdist=[]
            probs=[]

            mapnum=str(i)+str(q)
            actions,evidence,initx,inity=getData(mapnum)
            probgrid=[]
            for h in range(100):  # will be the rows, y var. map[y][x] map [row][col]
                tmprow = []
                for j in range(100):
                    if (tmpmap[h][j] == 'b'):
                        tmprow.append(0)
                    else:
                        tmprow.append(1 / 9000)

                probgrid.append(tmprow)

            paths = []
            for a in range(100):
                tmprow = []
                for b in range(100):
                    tmprow.append([(b, a)])
                paths.append(tmprow)
            count = 0
            rowprob=[]
            for a in range(100):
                probgrid, avg, maxx, maxy, rowprob = viterbi(actions, evidence, tmpmap, probgrid, count, paths)
                currx1,curry2=getLoc(str(i)+str(q),count)
                currx1 = int(float(currx1))
                curry2 = int(float(curry2))
                xmax, ymax, realxmax, realymax = getmax1(rowprob)
                ans, realans = getPath(count, xmax, ymax, realxmax, realymax,paths)
                curdist.append(dist(currx1,curry2,realxmax,realymax))
                count+=1
            distances.append(curdist)
    finaldist=[]
    finalprob=[]
    for z in range(100):
        tmpdist=0
        tmpprob=0
        for p in range(100):
            tmpdist+=distances[p][z]
        finaldist.append(tmpdist/100)
    print(finaldist)



def viterbi(actions,evidence,map,probgrid,count,paths):#a row will be the y, and the columns will be x. 2d arrays are [row][col] [y][x]
    ev=evidence[count]
    act=actions[count]
    max=0
    maxx=0
    maxy=0
    avg=0
    newgrid=[]
    rowprob=[]
    if(act=='r'):
        for count1, y in enumerate(map):#iterates rows/y
            tmpgridrow=[]
            for count2, x in enumerate(y):#iterates cols/x
                if(map[count1][count2]!='b'):#makes sure the block is not blocked
                    if(count2==0):#when moving right, we know it'll only be at 0/the border if movement fails, or theres a blocked
                        tmpval=probgrid[count1][count2]
                        if(map[count1][count2+1]!='b'):
                            v1=.1
                        else:
                            v1=1
                        if(ev!=map[count1][count2]):
                            v2=.05
                        else:
                            v2=.9
                        tmpgridrow.append(tmpval*v1*v2)
                        rowprob.append(tmpval*v1*v2)
                        avg+=(tmpval*v1*v2)
                        if(tmpval*v1*v2>max):
                            max=tmpval*v1*v2
                            maxx=count2
                            maxy=count1
                        paths[count1][count2].append((count2,count1))
                    else:# if the val is not at the left border
                        tmpval=probgrid[count1][count2]
                        if(ev!=map[count1][count2]):
                            v2=.05
                        else:
                            v2=.9
                        if(count2==99 or map[count1][count2+1]=='b'):#COUNT2+1 COULD CAUSE AN ERROR. MAKE SURE TO FIX IF IT DOES
                            v1=1
                        else:
                            v1=.1
                        newval=tmpval*v1*v2
                        stuff=0
                        if(map[count1][count2-1]!='b'):
                            v3=probgrid[count1][count2-1]
                            stuff=v3*.9*v2
                        if(stuff>newval):
                            tmpgridrow.append(stuff)
                            rowprob.append(stuff)
                            paths[count1][count2].append((count2-1,count1))
                        else:
                            tmpgridrow.append(newval)
                            rowprob.append(newval)
                            paths[count1][count2].append((count2,count1))
                        avg+=(newval)
                        if (newval > max):
                            max = newval
                            maxx=count2
                            maxy=count1
                else:
                    tmpgridrow.append(0)
                    rowprob.append(0)
            newgrid.append(tmpgridrow)
    elif(act=='l'):
        for count1, y in enumerate(map):#iterates rows/y
            tmpgridrow=[]
            for count2, x in enumerate(y):#iterates cols/x
                if(map[count1][count2]!='b'):
                    if(count2==99):
                        tmpval=probgrid[count1][count2]
                        if(map[count1][count2-1]=='b'):
                            v1=1
                        else:
                            v1=.1
                        if(ev!=map[count1][count2]):
                            v2=.05
                        else:
                            v2=.9
                        tmpgridrow.append(tmpval*v1*v2)
                        rowprob.append(tmpval*v1*v2)
                        paths[count1][count2].append((count2,count1))
                        avg+=(tmpval*v1*v2)
                        if (tmpval * v1 * v2 > max):
                            max = tmpval * v1 * v2
                            maxx = count2
                            maxy = count1
                    else:
                        tmpval=probgrid[count1][count2]
                        if(ev!=map[count1][count2]):
                            v2=.05
                        else:
                            v2=.9
                        if(count2==0 or map[count1][count2-1]=='b'):#COUNT2+1 COULD CAUSE AN ERROR. MAKE SURE TO FIX IF IT DOES
                            v1=1
                        else:
                            v1=.1
                        newval=tmpval*v1*v2
                        stuff=0
                        if(map[count1][count2+1]!='b'):
                            v3=probgrid[count1][count2+1]
                            stuff=v3*.9*v2
                        if(stuff>newval):
                            tmpgridrow.append(stuff)
                            rowprob.append(stuff)
                            paths[count1][count2].append((count2+1,count1))
                        else:
                            tmpgridrow.append(newval)
                            rowprob.append(newval)
                            paths[count1][count2].append((count2,count1))

                        avg+=(newval)
                        if (newval > max):
                            max = newval
                            maxx = count2
                            maxy = count1

                else:
                    tmpgridrow.append(0)
                    rowprob.append(0)

            newgrid.append(tmpgridrow)
    elif(act=='u'):
        for count1, y in enumerate(map):#iterates rows/y
            tmpgridrow=[]
            for count2, x in enumerate(y):#iterates cols/x
                if(map[count1][count2]!='b'):
                    if(count1==99):
                        tmpval=probgrid[count1][count2]
                        if(map[count1-1][count2]=='b'):
                            v1=1
                        else:
                            v1=.1
                        if(ev!=map[count1][count2]):
                            v2=.05
                        else:
                            v2=.9
                        tmpgridrow.append(tmpval*v1*v2)
                        rowprob.append(tmpval*v1*v2)
                        paths[count1][count2].append((count2,count1))
                        avg+=(tmpval*v1*v2)
                        if (tmpval * v1 * v2 > max):
                            max = tmpval * v1 * v2
                            maxx = count2
                            maxy = count1

                    else:
                        tmpval=probgrid[count1][count2]
                        if(ev!=map[count1][count2]):
                            v2=.05
                        else:
                            v2=.9
                        if(count1==0 or map[count1-1][count2]=='b'):
                            v1=1
                        else:
                            v1=.1
                        newval=tmpval*v1*v2
                        stuff=0
                        if(map[count1+1][count2]!='b'):
                            v3=probgrid[count1+1][count2]
                            stuff=v3*.9*v2
                        if(stuff>newval):
                            tmpgridrow.append(stuff)
                            rowprob.append(stuff)
                            paths[count1][count2].append((count2,count1+1))
                        else:
                            tmpgridrow.append(newval)
                            rowprob.append(newval)
                            paths[count1][count2].append((count2,count1))
                        avg+=(newval)
                        if (newval> max):
                            max = newval
                            maxx = count2
                            maxy = count1

                else:
                    tmpgridrow.append(0)
                    rowprob.append(0)

            newgrid.append(tmpgridrow)
    else:
        for count1, y in enumerate(map):#iterates rows/y
            tmpgridrow=[]
            for count2, x in enumerate(y):#iterates cols/x
                if(map[count1][count2]!='b'):
                    if(count1==0):
                        tmpval=probgrid[count1][count2]
                        if (map[count1+1][count2] != 'b'):
                            v1 = .1
                        else:
                            v1 = 1
                        if(ev!=map[count1][count2]):
                            v2=.05
                        else:
                            v2=.9
                        tmpgridrow.append(tmpval*v1*v2)
                        rowprob.append(tmpval*v1*v2)
                        paths[count1][count2].append((count2,count1))
                        avg+=(tmpval*v1*v2)
                        if (tmpval * v1 * v2 > max):
                            max = tmpval * v1 * v2
                            maxx = count2
                            maxy = count1

                    else:
                        tmpval=probgrid[count1][count2]
                        if(ev!=map[count1][count2]):
                            v2=.05
                        else:
                            v2=.9
                        if(count1==99 or map[count1+1][count2]=='b'):#COUNT2+1 COULD CAUSE AN ERROR. MAKE SURE TO FIX IF IT DOES
                            v1=1
                        else:
                            v1=.1
                        newval=tmpval*v1*v2
                        stuff=0
                        if(map[count1-1][count2]!='b'):
                            v3=probgrid[count1-1][count2]
                            stuff=v3*.9*v2
                        if(stuff>newval):
                            tmpgridrow.append(stuff)
                            rowprob.append(stuff)
                            paths[count1][count2].append((count2,count1-1))
                        else:
                            paths[count1][count2].append((count2,count1))
                            tmpgridrow.append(newval)
                            rowprob.append(newval)
                        avg+=newval
                        if (newval > max):
                            max = newval
                            maxx = count2
                            maxy = count1
                else:
                    tmpgridrow.append(0)
                    rowprob.append(0)

            newgrid.append(tmpgridrow)
    total=0
    for count1, a in enumerate(newgrid):
        for count2, b in enumerate(a):
            total+=newgrid[count1][count2]
    alpha=1/total
    #print(alpha)
    #print(newgrid)

    avg=avg/9000
    return newgrid,avg,maxx,maxy,rowprob



#runprog()
#USED TO GENERATE THE MAPS AND DATA
'''
for e in range(10):
    generateMap(e)
    map1 = takeMap(e)
    for f in range(10):
        generateData(map1,e,f)
'''
#generateMap()

mapnum=input("What map #?")
groundnum=input("What ground #?")
map1=takeMap(mapnum)
#runprog()RUN PROG
#generateData(map1)

actions,evidence,initx,inity=getData(groundnum)
probgrid=[]
rowprob=[]
for i in range(100):#will be the rows, y var. map[y][x] map [row][col]
    tmprow=[]
    for j in range(100):
        if(map1[i][j]=='b'):
            tmprow.append(0)
            rowprob.append(0)
        else:
            tmprow.append(1/9000)
            rowprob.append(1/9000)
    probgrid.append(tmprow)

paths=[]
for a in range(100):
    tmprow=[]
    for b in range(100):
        tmprow.append([(b,a)])
    paths.append(tmprow)

currx=initx
curry=inity
maxx=0
maxy=0
count=0
ans=[]
t0=time.time()
time1=[]
for i in range(0):
    tmptime=time.time()
    probgrid,avg,maxx,maxy,rowprob=viterbi(actions,evidence,map1,probgrid,count,paths)
    currx,curry=getLoc(groundnum,count)
    count+=1
    xmax, ymax,realxmax,realymax = getmax1(rowprob)
    ans,realans=getPath(count,xmax,ymax,realxmax,realymax,paths)
    time1.append(time.time()-tmptime)
print(time.time()-t0)
print(time1)


'''
for i in range(count):
    newx=paths[ymax][xmax][tmp][0]
    newy=paths[ymax][xmax][tmp][1]
    ans.append(paths[ymax][xmax][tmp])
    print(paths[ymax][xmax][tmp])
    ymax=newy
    xmax=newx

    tmp-=1
print(ans)
'''
#runprog()
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 10
HEIGHT = 6

# This sets the margin between each cell
MARGIN = 1

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.



# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [1250, 722]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Array Backed Grid")

# Loop until the user clicks the close button.
done = False #CHANGE TO FALSE TO DRAW GRID

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
font = pygame.font.Font(None, 10)
tmp1 = font.render('a', 1, (255, 0, 0))
postmp1=0
postmp2=0


# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            if(1100+100>pos[0]>1100 and 550+50>pos[1]>550):
                #print('hi')#call filter here
                if(count<100):
                    #print(count)
                    probgrid, avg, maxx, maxy,rowprob = viterbi(actions, evidence, map1, probgrid, count,paths)
                    currx,curry=getLoc(groundnum,count)
                    xmax, ymax, realxmax, realymax = getmax1(rowprob)
                    count += 1
                    ans,realans = getPath(count, xmax, ymax,realxmax,realymax,paths)
                    #print (ans)
                    print (realans)
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            # Set that location to one
            try:
                a=probgrid[row][column]
                tmp1 = font.render(str(a), 1, (255, 0, 0))
            except IndexError:
                pass
            font = pygame.font.Font(None, 14)
            #print("Click ", pos, "Grid coordinates: ", row, column)

    # Set the screen background
    screen.fill(BLACK)

    # Draw the grid
    for row in range(100):
        for column in range(100):
            if (map1[row][column] == 'b'):
                color = BLACK
            elif(str(row)==curry and str(column)==currx):
                color=(0,255,255)
            elif (row == maxy and column == maxx):
                color = (0, 0, 255)
            elif(probgrid[row][column]<avg):
                color = WHITE
            else:
                #color=RED
                color=WHITE

            pygame.draw.rect(screen,color,[(MARGIN + WIDTH) * column + MARGIN,(MARGIN + HEIGHT) * row + MARGIN,WIDTH,HEIGHT])

    # Limit to 60 frames per second

    for abc in ans:
        for box in abc:
            if(box[0]!=currx and box[1]!=curry):
                pygame.draw.rect(screen, (0,100,0),
                             [(MARGIN + WIDTH) * box[0] + MARGIN, (MARGIN + HEIGHT) * box[1] + MARGIN, WIDTH, HEIGHT])

    for val in realans:
        if(val[0]!=currx and val[1]!=curry):
            pygame.draw.rect(screen, (0, 255, 0),
                             [(MARGIN + WIDTH) * val[0] + MARGIN, (MARGIN + HEIGHT) * val[1] + MARGIN, WIDTH, HEIGHT])

    pygame.draw.rect(screen,(0,255,255),[(MARGIN + WIDTH) * int(currx) + MARGIN, (MARGIN + HEIGHT) * int(curry) + MARGIN, WIDTH, HEIGHT])
    clock.tick(60)

    pygame.draw.rect(screen,GREEN,(1100,550,100,50))
    for i in range(100):
        tmp2 = font.render(str(i), 1, (255, 0, 0))
        screen.blit(tmp2,(1100,(i+.2)*7))
        tmp3=font.render(str(i),1,(255,0,0))
        screen.blit(tmp3,((i)*11,700))
    screen.blit(tmp1, (1125,10))
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()