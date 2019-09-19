#TODO make this more efficient + use delay when crawling/scrapping
#
#build bipartite graph showing show date and people who appeared 
#
#node set A: show date/number
#node set B: people who appeared
#connect an edge from show i to person j if person j was on show i 

#will store: show-dates.txt, people.txt, showdates-people.smat

import requests
from bs4 import BeautifulSoup 
import re 


def removeNamePrefix(name):
    '''correct names starting w/ salutation or containing quotes'''
    prefixes = ['Dr.','Rep.', 'Sen.','Senator','Maj.','Lt. Col.','Col.','Brig. Gen.','Sgt.',
                'Gov.','Rev.','Rep.-elect', 'Major','Maj. Gen.','Lt.','Sgt. Maj.','Capt.',
                'Lieutenant Colonel','Chef', 'Fmr. Rep.','Rep.','brig.', 'lieutenant',
                'colonel','fmr.','gen.', 'bishop']
    
    prefixes = list(map(lambda x:x.lower(),prefixes))
    try:
        #if name has space and there's a prefix then remove it
        ind = name.index(' ')
        first = name[:ind].lower()
        
        while first in prefixes:
            name = name[ind+1:]
            try:
                ind = name.index(' ')
                first = name[:ind].lower()
            except:
                break            
    except:
        return name

    return name



website = 'http://www.msnbc.com/transcripts/rachel-maddow-show'
#years for which transcripts are available
#from sep 2008 to sep 2019 (9/18/2019 around 10:30 PM eastern time)

#building list of urls #urls look like url/year/month
urls = [website+'/'+str(year)+'/'+str(month) for year in range(2009,2019) for month in range(1,13)]
urls += [website+'/'+str(2008)+'/'+str(month) for month in range(9,13)]
urls += [website+'/'+str(2019)+'/'+str(month) for month in range(1,10)]


#want to collect people and show dates
hyperedges = []
dates = []

splitters=re.compile('[:;,]+')
strip_whitespace = re.compile('[^\s]+')

pattern=re.compile('[^,\s]+')

for i,link in enumerate(urls):
    print(str(i)+' of '+str(len(urls)-1))
    page = requests.get(link)
    soup = BeautifulSoup(page.text,'html.parser')
    
    tag = soup.find_all('div',attrs={'class':'field field-name-field-short-summary field-type-text field-label-inline inline'})
    
    for item in tag:
        #get date
        temp = (item.parent).descendants
        next(temp)
        date = next(temp)
        
        #build canonical date format        
        monthDayYear = re.findall(pattern,date.lower())[1:]    
        months = {'january':'01','february':'02','march':'03','april':'04','may':'05',
                  'june':'06','july':'07','august':'08','september':'09','october':'10',
                  'november':'11','december':'12'}
            
        if int(monthDayYear[1])<10:    
            date = months[monthDayYear[0]]+'-0'+ monthDayYear[1]+'-'+monthDayYear[-1]
        else:
            date = months[monthDayYear[0]]+'-'+monthDayYear[1]+'-'+monthDayYear[-1]    
        dates.append(date)
              
        #get guest information
        guestList = item.descendants
        real_names = []
        
        #processing names
        for guestStr in guestList:
            #split string by guest
            guests = re.split(splitters,guestStr)
            
            for name in guests:
                #peel away whitespace
                striped_name = re.findall(strip_whitespace,name)
                
                #build canonical name
                n=''
                for k in striped_name:
                    n += k
                    n += ' '
                    
                n = n[:-1]
                
                n = n.lower()#lowercase
                n = removeNamePrefix(n)#remove prefixes
                                                
                ###make corrections                
                corrections = {'dabo adegbile' : 'debo adegbile'  ,  
                    'mike almy' : 'michael almy',
                    'matt axelrod' : 'matthew axelrod',
                    'jared bernstein' : 'jarred bernstein',
                    'bon borelli' : 'don borelli',
                    'cornell brooks' : 'cornell william brooks',
                    'glen caplin' : 'glenn caplin',
                    'dan choi' : 'daniel choi',
                    'marq claxton' : 'marquez claxton',
                    'nick confessore' : 'nicholas confessore',
                    'bob costa' : 'robert costa',
                    'ana maria cox' : 'ana marie cox',
                    'pete defazio' : 'peter defazio',
                    'thomas d`agostino' : 'thomas d‘agostino',
                    'norm eisen' : 'norman eisen',
                    'elizabeth est' : 'elizabeth esty',
                    'melissa falkowsji' : 'melissa falkowski',
                    'fehrenbach' : 'victor fehrenbach',                    
                    'tom frank' : 'thomas frank',
                    'welton gaddy' : 'c. welton gaddy',
                    'james galbraith' : 'james k. galbraith',
                    'ann gearan' : 'anne gearan',
                    'tom goldstein' : 'thomas goldstein',                    
                    'bob greenstein' : 'robert greenstein',
                    'jaime harrison' : 'jamie harrison',
                    'chris hayes' : 'christopher hayes',
                    'ryan haygood' : 'ryan p. haygood',
                    'steve horsford' : 'steven horsford',
                    'mike isikoff' : 'michael isikoff',
                    'ben jealous' : 'benjamin todd jealous',
                    'cristina jiminez' : 'cristina jimenez',
                    'cleave jones' : 'cleve jones',
                    'bill keating' : 'william keating',
                    'nancy keegan' : 'nancy keenan',
                    'evan kohlman' : 'evan kohlmann',
                    'josh koskoff' : 'joshua koskoff',
                    'chris lu' : 'christopher lu',
                    'ed lyman' : 'edwin lyman',
                    'dan malloy' : 'dannel malloy',
                    't. martin' : 'ti martin',
                    'mike mcfaul' : 'michael mcfaul' ,
                    'jim mcgovern' : 'james mcgovern',
                    'joe mcquaid' : 'joseph mcquaid',
                    'bob menendez' : 'robert menendez',
                    'matt miller' : 'matthew miller',
                    'eric mouthaan' : 'erik mouthaan',
                    'ion nissenbaum' : 'dion nissenbaum',
                    'rebecca o`brien' : 'rebecca davis o`brien',
                    'tim o`brien' : 'timothy o`brien',
                    'ned price' : 'edward price',
                    'jon ralston' : 'john ralston',
                    'cecile richard' : 'cecile richards',
                    'tom ritchie' : 'thomas ritchie',
                    'dan roberts' : 'david roberts',#double check this one
                    'gene robinson' : 'eugene robinson',
                    'mudcat saunders' : 'dave “mudcat” saunders',
                    'chuck schumer' : 'charles schumer',
                    'jeff sharlett' : 'jeff sharlet',
                    'gabe sherman' : 'gabriel sherman',
                    'kathy spillar' : 'katherine spillar',
                    'ann thompson' : 'anne thompson',
                    'mike viquiera' : 'mike viqueira', 
                    'nicole wallace' : 'nicolle wallace',
                    'debbie wasserman schultz' : 'debbie wasserman-schultz',
                    'clint watts' : 'clinton watts',
                    'dough wead' : 'doug wead',
                    'dave weigel' : 'david weigel',
                    'larry wilkerson' : 'lawrence wilkerson',
                    'ben wittes' : 'brnjamin wittes',
                    'bill wolf' : 'bill wolff',
                    'matt yglesias' : 'matthew yglesias',
                    'jeff zremski' : 'jerry zremski',
                    'james roosevelt' : 'james roosevelt jr.',
                    'ken ward' : 'ken ward jr.'}
                    
            
                if n in corrections.keys():
                    n = corrections[n]
                
                badEntries = ['n/a','','guest','guests','jr.']
            
                #handling missing + bad entries
                if n=='eugene robinson sen. claire mccaskill':
                    real_names.append('eugene robinson')
                    real_names.append('claire mccaskill')
                elif n == 'kent jones lawrence wilkerson':
                    real_names.append('kent jones')
                    real_names.append('lawrence wilkerson')
                elif n == 'ken dilanian and betsy woodruff':
                    real_names.append('ken dilanian')
                    real_names.append('betsy woodruff')
                elif n in badEntries:
                    pass
                else:
                    real_names.append(n)
                
                    
            hyperedges.append(real_names)
                
#error checking
print(len(dates)==len(hyperedges))


nDateNodes = len(dates)
           

#hash names
names = []
for edge in hyperedges:
    names += edge
    
people = list(set(names))#for people.txt
nameMap = {people[k]:nDateNodes + k for k in range(len(people))}

#sorting in chronological order
dates,hyperedges = zip(*sorted(zip(dates,hyperedges),key = lambda x:x[0][-4:]+x[0][:2]+x[0][3:5]))

hashedEdges = list(map(lambda x: [nameMap[x[i]] for i in range(len(x))],hyperedges))

dateMap = {dates[k]:k for k in range(len(dates))}
hashedDates = list(map( lambda x: dateMap[x],dates))

#write dates,people + edges to files 
with open('people.labels','w') as fptr:
    for person in people:
        fptr.write('%s\n' %person)

with open('show-dates.labels','w') as fptr:
    for date in dates:
        fptr.write('%s\n' %date)
    

edges = []
for index in hashedDates:
    for e in hashedEdges[index]:
        edges.append((index,e))
        edges.append((e,index))
edges = sorted(edges)
        
totalNodes = len(dates)+len(people)

with open('maddow-show-edges.smat',mode='w') as fptr:
    fptr.write('{0:d}\t{1:d}\t{2:d}\n'.format(totalNodes,totalNodes,len(edges)))
    for i in range(len(edges)):
        fptr.write('{0:d}\t{1:d}\t{2:d}\n'.format(edges[i][0],edges[i][1],1))
    