import matplotlib.pylab as plt
import webbrowser

class SH:
    def __init__(self,tourname,graphname):
        self.tname=tourname
        self.gname=graphname
        self.tour=self.readTour()
        (self.graph,self.order)=self.readGraph()#one direction graph & index of the cities
        self.count=len(self.order)#number of cities
        self.dis=self.countDis()#graph used in calculation

        #Required to plot shortest path on a Google Map
        self.finalPathOrder = []
        self.coordinateFile = 'LatLong_50cities.csv'
        self.coordinateList = []

    # This method is used for reading a coordinates file and plotting the results of the Djikstra's algorithm on the Map using HTML/Javascript
    def map(self):
        #self.coordinateList[]

        # For Google Map
        plotCities = []

        # Call the method to read the coordinate file
        self.readLatLong()
        for i in self.finalPathOrder:
            #print(self.order[i])
            for j in self.coordinateList:
                if self.order[i].upper().lstrip() == j[0].upper().rstrip():
                    plotCities.append(j)

        # Building the coordinates for each city to add in Javascript
        totalLatitude  = 0
        totalLongitude = 0
        cord=''
        for city in plotCities:
            #print(city)
            cord += 'new google.maps.LatLng('+city[1]+','+city[2]+'),'
            totalLatitude += float(city[1])
            totalLongitude += float(city[2])

        # Latitude and Longitude for home/ default zoom
        homeLat =  totalLatitude/len(plotCities)
        homeLong = totalLongitude/len(plotCities)
        lat = '39.0997'
        long = '-94.5786'

        # HTML/Javascript for rendering the map and plotting the path
        body = """<!DOCTYPE html>
                    <html>
                      <head>
                        <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
                        <meta charset="utf-8">
                        <title>Animating Symbols</title>
                        <style>
                          html, body {
                            height: 100%;
                            margin: 0;
                            padding: 0;
                          }
                          #map {
                            height: 99%;
                            width: 99%;
                          }
                        </style>
                            <script src="https://maps.googleapis.com/maps/api/js?&callback=initMap&signed_in=true" async defer>
                        </script>
                         <script>


                    function initMap() {
                      var homeLatlng = new google.maps.LatLng(""" + str(homeLat) + ""","""+ str(homeLong) + """);
                      var map = new google.maps.Map(document.getElementById('map'), {
                        center: homeLatlng,
                        zoom: 6,
                        mapTypeId: google.maps.MapTypeId.ROADMAP
                      });

                      var lineSymbol = {
                        path: google.maps.SymbolPath.CIRCLE,
                        scale: 8,
                        strokeColor: '#393'
                      };

                      var line = new google.maps.Polyline({
                        path: [""" + cord + """],
                        icons: [{
                          icon: lineSymbol,
                          offset: '100%'
                        }],
                        map: map
                      });

                      animateCircle(line);
                    }

                    function animateCircle(line) {
                        var count = 0;
                        window.setInterval(function() {
                          count = (count + 1) % 500;
                          var icons = line.get('icons');
                          icons[0].offset = (count / 5) + '%';
                          line.set('icons', icons);
                      }, 20);
                    }
                        </script>
                      </head>
                      <body>
                        <div id="map"></div>
                      </body>
                    </html> """

        f = open('mapAnimated.html','w')
        f.write(body)
        f.close()
        webbrowser.open_new_tab('mapAnimated.html')
        print('Map loaded in browser')

    # This Method reads the coordinate File and storing the results in a list to be used while rendering the Map
    def readLatLong(self):
        fHandle = open(self.coordinateFile,'r')
        cList = []
        for line in fHandle:
            newline = line.rstrip('\n')
            alist = newline.split(',')
            cList.append(alist)
        fHandle.close()
        self.coordinateList = cList

    # This method reads the Tour files in a list
    def readTour(self):
        f=open(self.tname,'r')
        bList=[]
        for line in f:
            aList=line.split(';')
            for i in range(0,len(aList)):
                aList[i]=aList[i].rstrip('\n')
            bList.append(aList)
        f.close()
        return bList

# This method returns a list of valid path(only one direction recorded)
#and a list of city name
    def readGraph(self):
        f=open(self.gname,'r')
        validroad=[]
        city=f.readline()
        cityorder=[]
        citySplit=city.split(';')
        citySplit[len(citySplit)-1]=citySplit[len(citySplit)-1].rstrip('\n')
        del citySplit[0]
        for city in citySplit:
            c = city.strip()    # Stripping any white spaces from city names on both sides if any
            cityorder.append(c)
        for line in f:
            bList=[]
            aList=line.split(';')
            for i in range(0,len(aList)):
                aList[i]=aList[i].rstrip('\n')
                if aList[i]=='1':
                    bList.append(i-1)
            validroad.append(bList)
        f.close()
        return (validroad,cityorder)

# Get the coordinates of a city, return a list[x,y]
    def coordinates(self,cityNum):
        co=[]
        co.append(int(self.tour[cityNum][1]))
        co.append(int(self.tour[cityNum][2]))
        return co

# Get the (order)Number of a city
    def getCityNum(self,city):
        for i in range(0,self.count):
            if city.upper()==self.order[i].upper():
                return i

# Draw all the valid roads
    def drawRoads(self):
        for i in range(0,len(self.graph)):
            for j in self.graph[i]:
                c1=self.coordinates(i)
                c2=self.coordinates(j)
                plt.plot(c1[0],c1[1],'or')
                plt.plot(c2[0],c2[1],'or')       
                plt.plot((c1[0],c2[0]),(c1[1],c2[1]),'k--')

# Draw the shortest path between two cities
    def drawPath(self,start,end,path):
        x=[]
        y=[]
        #q = list of citynums in path between start & end (inclusive)
        q=[end]
        while end!=start:
            x.append(self.coordinates(end)[0])
            y.append(self.coordinates(end)[1])
            end=path[end]
            q.append(end)
        x.append(self.coordinates(start)[0])
        y.append(self.coordinates(start)[1])
        # z = reference to make q iterable (otherwise it produces an error)
        z=q

        # Storing city order for plotting on Google Maps
        pathOrder = list(z)
        pathOrder.reverse()
        #self.finalPathOrder = list(pathOrder)
        self.finalPathOrder.extend(pathOrder)

        xx=[]
        yy=[]
        for i in range(0,len(x)-1):
            q=abs((x[i]-x[i+1])/2) + min(x[i],x[i+1])
            w=abs((y[i]-y[i+1])/2) + min (y[i],y[i+1])
            xx.append(q)
            yy.append(w)
        #print path distances between each city on route
        for i in range(0,len(xx)):
            plt.text(xx[i],yy[i],round(self.dis[z[i]][z[i+1]],2),
                    color='k',
                    size=7,
                    bbox={'facecolor':'white','alpha':1})
        #print name of each city on route
        for i in range(0,len(z)):
            plt.text(x[i]+0.25,y[i]+0.25,self.order[z[i]],color='k',
                    style='oblique',
                    size=7,
                    bbox={'facecolor':'white','alpha':0.7})
        plt.plot(x,y,'blue',linewidth=2)

# Print the shortest path between two cities             
    def printPath(self,start,end,path):
        p=[]
        d=[]
        s=''
        while end!=start:
            last=path[end]
            d.append(self.dis[end][last])
            p.append(self.order[end])
            end=last
        p.append(self.order[start])
        for i in range(0,len(p)-1):
            s+=p[len(p)-i-1]+'--'+str(d[len(d)-i-1])+'-->'
        s+=p[0]
        print(s)
        
# Return a dictionary storing valid distance(both direction)
    def countDis(self):
        disAll={}
        for i in range(0,self.count):
            disRow={}
            disAll[i]=disRow
            for j in self.graph[i]:
                c1=self.coordinates(i)
                c2=self.coordinates(j)
                dis=((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)**(1/2)
                disRow[j]=dis
                disAll[j][i]=dis
                disAll[i]=disRow
        return disAll

# Dijkstra's algorithm
#parameters: (dictionary)valid distance, starting city,number of cities and the not valid distance(just for easier generalization)
    def Dijkstra(self,graph,start,n,notValid=1000):
        Seen=set()
        Unseen=set(range(0,n))
        sh=[notValid]*n#list of shortest distance
        prev=[notValid]*n#list of previous city
        
        #initialize
        sh[start]=0
        prev[start]=start
        Seen.add(start)
        Unseen.remove(start)
        minv=0
        middle=start#take the start point as the middle point
        
        #search through the cities
        try:
            while len(Unseen)!=0:
                tmp=notValid
                for i in Unseen:
                    if i in graph[middle].keys():
                        #update the distances
                        if minv+graph[middle][i]<sh[i]:
                            sh[i]=minv+graph[middle][i]
                            prev[i]=middle
                    #find the next shortest path
                    if sh[i]<tmp:
                        tmp=sh[i]
                        k=i
                #do not search the city again
                Seen.add(k)
                Unseen.remove(k)
                middle=k
                minv=tmp
            return[sh,prev]
        except Exception as ex:
            print(ex)

# A test method(not for the answer)
    def test(self):
        graph={0:{1:6,2:3},
               1:{0:6,2:2,3:5},
               2:{0:3,1:2,3:3,4:4},
               3:{1:5,2:3,4:2,5:3},
               4:{2:4,3:2,5:5},
               5:{3:3,4:5}}
        #result=self.Dijkstra(graph,0,6)
        #print(self.Yen(self.dis,1,0,K=2))
        self.kthShortest(1,0,K=4)

# Interactive with user, get the city name
    def typeIn(self, startCity=None, endCity=None):
        try:
            s=''
            #start city
            if startCity!=None:
                start=self.getCityNum(startCity)
            else:
                s=input('Start from:').strip()
                while s!='e':
                    start=self.getCityNum(s)
                    if start==None:
                        s=input('Please type in the proper city name:').strip()
                    else:
                        break
            #end city                       
            if endCity!=None:
                end=self.getCityNum(endCity)
            else:
                s=input('To:').strip()
                while s!='e':
                    end=self.getCityNum(s)
                    if end==None:
                        s=input('Please type in the proper city name:').strip()
                    else:
                        break
            return (start,end)
        except Exception as ex:
            print(ex)
            
# Return a path given the list of previous city and start&end
    def toPath(self,prev,start,end):
        path=[]
        while end!=start:
            path.append(end)
            last=prev[end]
            end=last
        path.append(start)
        path.reverse()
        return path

# ExtraCredit Problem 1
    def kthShortest(self):
        start,end=self.typeIn()
        while True:
            try:
                K=input('K=').strip()
                if K.isnumeric():
                    K=int(K)
                    break
            except Exception as ex:
                print(ex)               
        result=self.Yen(self.dis,start,end,K)
        print('All the',K,'-shortest paths are:')
        q=[]
        for i in range(len(result)):
            s=''
            for city in result[i][0]:
                s+=self.order[city]+'===>'
                q=result[i][0]
            print('[',i,']:',s,'Total distance is',result[i][1][end])
        print('\nThe shortest ',K,'th path is:[',i,']')

        #visualize
        #print('q:',q)
        self.drawRoads()
        x=[]
        y=[]
        for cityNum in result[i][0]:
            x.append(int(self.tour[cityNum][1]))
            y.append(int(self.tour[cityNum][2]))
        # z = reference to make q iterable (otherwise it produces an error)
        z=q

        # Storing city order for plotting on Google Maps
        pathOrder = list(z)
        #pathOrder.reverse()
        #self.finalPathOrder = list(pathOrder)
        self.finalPathOrder.extend(pathOrder)

        xx=[]
        yy=[]
        for i in range(0,len(x)-1):
            q=abs((x[i]-x[i+1])/2) + min(x[i],x[i+1])
            w=abs((y[i]-y[i+1])/2) + min (y[i],y[i+1])
            xx.append(q)
            yy.append(w)
        #print path distances between each city on route
        for i in range(0,len(xx)):
            plt.text(xx[i],yy[i],round(self.dis[z[i]][z[i+1]],2),
                    color='k',
                     size=7,
                    bbox={'facecolor':'white','alpha':1})
        #print name of each city on route
        for i in range(0,len(z)):
            plt.text(x[i]+0.25,y[i]+0.25,self.order[z[i]],color='k',
                    style='oblique',
                    size=7,
                    bbox={'facecolor':'white','alpha':0.7})
        plt.plot(x,y,'blue',linewidth=2)
        print('')
        print('Close the Plot to see the path in Google Maps')
        plt.show()
            
# Yen's Algorithm(rewrite based on the understanding of the existing code)
    def Yen(self,graph,start,end,K=1,notValid=1000):
        #the queue, store the confirmed path(state) by order
        A=[]
        #store the potential path to sort
        B=[]
        #Find the shortest path to be first state
        result=self.Dijkstra(graph,start,self.count)
        dist=result[0]
        prev=result[1]
        #return None if there is no way between start and end
        #put the state(path,dist) into the queue
        if prev[end]!=notValid:
            A.append((self.toPath(prev,start,end),dist))
        else:
            return None
        
        for k in range(1,K):
            #take out the last state(the solution of k-1 th shortest)
            last_path=A[-1][0]
            last_dist=A[-1][1]
            
            #for different spur node v between start and end
            #total_path=(start-->v)root_path+(v-->end)spur_path
            for v in range(0,len(last_path)-1):
                spur_node=last_path[v]
                root_path=last_path[:v+1]
                root_distance=last_dist[spur_node]       
            #find a new v-->end path
                #remove next edges from spur node(v-->u) that appear in the pervious
                #states which share the same root path
                #otherwise will get the same spur_path as before
                edges_removed=[]
                for states in A:
                    path=states[0]
                    if(len(path)>v+1 and path[:v+1]==root_path and path[v+1] in graph[spur_node]):
                        #store and remove(node v,node u,w(v,u))
                        edges_removed.append((spur_node,path[v+1],graph[spur_node].pop(path[v+1])))    
                #calculate the new spur path(v-->u'-->end)
                result=self.Dijkstra(graph,spur_node,self.count)
                #if exist,store the new completed path into B
                if result:
                    dist=result[0]
                    prev=result[1]
                    if prev[end]!=notValid:
                        #new total_path=root_path+new spur_path
                        total_path=root_path[:-1]+self.toPath(prev,spur_node,end)
                        #distance of nodes in root_path did not change,after spur_node changed
                        total_dist=[notValid]*len(last_dist)
                        for node in range(0,len(dist)):
                            if node in root_path:
                                total_dist[node]=last_dist[node]
                            total_dist[node]=dist[node]+root_distance
                        if(total_path,total_dist) not in B:
                            B.append((total_path,total_dist)) 
                #add back the edges and nodes that were removed from the graph.
                for edge in edges_removed:
                    graph[edge[0]][edge[1]]=edge[2]
                    
        #put the possible kth shortest path into the queue
            if B:
                B.sort(key=lambda p:p[1][end])#sort out the shortest one
                A.append(B.pop(0))
            else:
                break
        return A
        
# Basic Problem + ExtraCredit Problem 2
    def CertainCity(self):
        print("-------------------------------------")
        notValid = 1000
        print("Do you have a certain city to pass?")
        passIf=''
        judge = True
        # Ask users if they want to pass a certain city
        while (judge):
            if passIf!='YES' and passIf!='NO':
                passIf=input('Please type in YES or NO:').upper().strip()
            else:
                break
        # Users do not want to pass a certain city
        if passIf == 'NO':
            #Call typeIn() and return the start and end cities.
            (start,end)=self.typeIn()
            result=self.Dijkstra(self.dis,start,self.count,notValid)
            self.drawRoads()
            if result[0][end]<notValid:
                self.drawPath(start,end,result[1])
                self.printPath(start,end,result[1])
                print('The shortest distance between the two cities is: ',result[0][end])
            else:
                print('No such path exists.')
        # Users want to pass a certain city
        else:
            s = input('Please input the certain city you want to pass:').strip()
            while s!='e':
                    passCity=self.getCityNum(s)
                    if passCity!=None:
                        break
                    else:
                        s=input('Please type in the proper city name:').strip()
            #Journey 1: typeIn() return start city and "end city" is passing city
            (start1,end1)=self.typeIn(None,s)
            result1=self.Dijkstra(self.dis,start1,self.count,notValid)
            self.drawRoads()
            #Journey 2: typeIn() return "start city" (passing city) and end city
            (start2,end2)=self.typeIn(s,None)
            result2=self.Dijkstra(self.dis,start2,self.count,notValid)
            self.drawRoads()

            if result1[0][end1]<notValid and result2[0][end2]<notValid:
                # print out the result
                print('-------------------------------------')
                print('Result:')
                # print the first journey
                self.drawPath(start1,end1,result1[1])
                self.printPath(start1,end1,result1[1])
                # print the second journey
                self.drawPath(start2,end2,result2[1])
                self.printPath(start2,end2,result2[1])
                
                print('The shortest distance between the two cities is: ',result1[0][end1]+result2[0][end2])
            else:
                print('No such path exists.')

        print('')
        print('Close the Plot to see the path in Google Maps')
        plt.show()

    def main(self):

        while True:
            #print welcome message
            print('Hi, welcome to shortest path calculator!')
            print('Here are the available cities!')
            print(self.order)
            print('-------------------------------------')
            print("What do you want to do?")
            print('1: search the shortest path\n2: search the Kth shortest path\n3: Exit')

            search = input("Please input '1','2',or '3':").upper().strip()
            if (search=='1'):
                # Search for the shortest path
                self.CertainCity()
                self.map()
                self.finalPathOrder.clear() # Clearing the path List for reuse
                #print('Press Enter to run the shortest path calculator again')
                print('*********************************************************')
                inp = input('Hit Enter to run the shortest path calculator again')
                print('\n')

            elif(search=='2'):
                # Searching for k-th shortest path
                self.kthShortest()
                self.map()
                self.finalPathOrder.clear() # Clearing the path List for reuse
                print('*********************************************************')
                inp = input('Hit Enter to run the shortest path calculator again')
                print('\n')

            elif (search=='3'):
                # Exit program
                print('**********PROGRAM EXITED*************')
                break
            
            
if __name__ == "__main__":
    sh=SH('tour.csv','graph.csv')
    sh.main()
    # sh.map()
    # webbrowser.open_new_tab('boston.html')



