###############################
#                             #
#	wagc_points.py            #
#	Reinhardt Messerschmidt   #
#	2006-10-22                #
#                             #
###############################

#The script has three sections:
#1. Read parameters
#2.	Define class player
#3. Main
#
#The main section sets up a dictionary ("players") that uses players' names as keys and instances of the class "player" as values. It 
#then reads the data and calls methods of the class "player" to do the calculations.

import os
import sys

##########################
#	1. Read parameters   #
##########################

#open parameter file
fparam=sys.argv[1]
f=open(fparam)

#read annual depreciation parameter
dep=float(f.readline())
f.readline()

#read representative's depreciation parameter
rep=int(f.readline())
f.readline()

#read membership points parameter
mem=int(f.readline())
f.readline()

#read SA championship points parameters
place=[]
line=f.readline()
while line.strip()<>'*':
    place.append(int(line))
    line=f.readline()
place_top=len(place)-1

#read internet championship points parameters
inet=[]
inet_maxtour=int(f.readline())
line=f.readline()
while line.strip()<>'*':
    inet.append(int(line))
    line=f.readline()
inet_top=len(inet)-1

#read participation points parameters
part_max_tot=int(f.readline())
part_max_opp=int(f.readline())
part={}
part['t']=int(f.readline())
part['c']=int(f.readline())
part['i']=int(f.readline())
f.close()  

##############################
#   2. Define class player   #
##############################

class player:
    
    #initialize
    def __init__(self, name, lyom, open):
        
        #name
        self.name=name
        
        #last year of membership
        self.lyom=lyom
        
        #opening balance
        self.open=open
        
        #annual depreciation
        self.dep=int(-round(dep*self.open))
        
        #representative's depreciation
        self.rep=0
        
        #membership points
        self.mem=0
        
        #SA championship points
        self.place=0
        
        #internet championship points
        self.inet=0
        self.inet_list=[]
        
        #paticipation points
        self.part=0
        self.part_list=[]
        
        #closing balance
        self.close=0
        
    #get string representation
    def __str__(self):
        return self.name+','+self.lyom+','+str(self.open)+','+str(self.dep)+','+str(self.rep)+','+str(self.mem)+','+str(self.place)+','+str(self.inet)+','+str(self.part)+','+str(self.close)
    
    #compare
    def __cmp__(self,other):
        if self.close<other.close:
            return -1
        elif self.close==other.close:
            return 0
        else:
            return 1
    
    #set last year of membership
    def set_lyom(self,lyom):
        self.lyom=lyom
        
    #is member?
    def is_mem(self):
        return self.lyom==year
        
    #calculate membership points
    def calc_mem(self):
        self.mem=mem
        
    #calculate representative's depreciation
    def calc_rep(self,s,n,p,t):
        self.rep=-int(min(round(1000*(n+2*float(s)/100)-1000*(float(t)-p)/(t-1)),rep))
    
    #calculate SA championship points
    def calc_place(self,pos=-1,tie=1):
        if self.is_mem():
            if pos==-1:
                self.place=place[-1]
            else:
                if pos+tie<=place_top:
                    shared=reduce(lambda x,y: x+y,place[pos:pos+tie])
                elif pos<place_top and top<=pos+tie:
                    shared=reduce(lambda x,y: x+y,place[pos:place_top])+(pos+tie-place_top)*place[-1]
                elif inet_top<=pos:
                    shared=tie*place[-1]
                self.place=int(round(float(shared)/tie))
                
    #calculate internet championship points
    def calc_inet(self,pos=-1,tie=1):
        if pos==-1 or not self.is_mem():
            self.inet_list.append(0)
        else:
            if pos==-1:
                self.inet_list.append(0)
            else:
                if pos+tie<=inet_top:
                    shared=reduce(lambda x,y: x+y,inet[pos:pos+tie])
                elif pos<inet_top and top<=pos+tie:
                    shared=reduce(lambda x,y: x+y,inet[pos:inet_top])+(pos+tie-inet_top)*inet[-1]
                elif inet_top<=pos:
                    shared=tie*inet[-1]
                self.inet_list.append(int(round(float(shared)/tie)))
                
            copy=[]
            for x in self.inet_list:
            	copy.append(x)
            copy.sort()
            copy.reverse()
            self.inet=reduce(lambda x,y: x+y,copy[0:inet_maxtour])
        
    #calculate participation points
    def calc_part(self,date,opp,type):
        if self.is_mem():
            if type=='t' or type=='c' or type=="i":#(type=='i' and opp.is_mem()):
                if len(self.part_list)==0:
                    self.part_list.append([date,opp.name,type,part[type],part[type],part[type]])
                else:
                    cum_tot=self.part_list[-1][-1]
                    found=0
                    i=len(self.part_list)
                    while not found and i>0:
                        i=i-1 
                        if self.part_list[i][1]==opp.name:
                           found=1
                    if found:
                        cum_opp=self.part_list[i][4]
                    else:
                        cum_opp=0
                    points=min(part_max_tot-cum_tot,part_max_opp-cum_opp,part[type])    
                    self.part_list.append([date,opp.name,type,points,cum_opp+points,cum_tot+points])
            self.part=self.part_list[-1][-1]
    
    #calculate closing balance
    def calc_close(self):
        self.close=max(self.open+self.dep+self.rep+self.mem+self.place+self.inet+self.part,0)
        
    #create report
    def report(self):
        lines=[]
        w1=40
        w2=5
        w=w1+w2
        lines.append('-'*w+'\n')
        lines.append(('WAGC points for '+self.name).ljust(w)+'\n')
        lines.append('-'*w+'\n')
        lines.append((year+' opening balance:').ljust(w1)+str(self.open).rjust(w2)+'\n')
        lines.append(('Annual depreciation:').ljust(w1)+str(self.dep).rjust(w2)+'\n')
        lines.append(('Representative\'s depreciation:').ljust(w1)+str(self.rep).rjust(w2)+'\n')
        lines.append(('Membership points:').ljust(w1)+str(self.mem).rjust(w2)+'\n')
        lines.append(('SA Championship points:').ljust(w1)+str(self.place).rjust(w2)+'\n')
        lines.append(('Internet Championship points:').ljust(w1)+str(self.inet).rjust(w2)+'\n')
        lines.append(('Participation points:').ljust(w1)+str(self.part).rjust(w2)+'\n')
        lines.append('-'*w+'\n')
        lines.append((year+' closing balance:').ljust(w1)+str(self.close).rjust(w2)+'\n')
        lines.append('-'*w+'\n')
        lines.append('\n')
        lines.append('\n')
        lines.append('\n')
                
        w1=40
        w2=5
        w=w1+w2
        lines.append('-'*w+'\n')
        lines.append('Exposition of Internet Championship points'.ljust(w)+'\n')
        lines.append('-'*w+'\n')
        for i in range(len(self.inet_list)):
            lines.append(('Tournament '+str(i+1)).ljust(w1)+str(self.inet_list[i]).rjust(w2)+'\n')
        lines.append('-'*w+'\n')
        lines.append(('Sum of '+str(inet_maxtour)+' best results:').ljust(w1)+str(self.inet).rjust(w2)+'\n')
        lines.append('-'*w+'\n')
        lines.append('\n')
        lines.append('\n')
        lines.append('\n')
                
        w1=12
        w2=30
        w3=6
        w=w1+w2+w3*4
        lines.append('-'*w+'\n')
        lines.append('Exposition of participation points'.ljust(w)+'\n')
        lines.append('-'*w+'\n')
        lines.append(''.ljust(w1+w2)+'Game'.rjust(w3)+'Part'.rjust(w3)+'Cum'.rjust(w3)+'Cum'.rjust(w3)+'\n')
        lines.append('Date'.ljust(w1)+'Opponent'.ljust(w2)+'type'.rjust(w3)+'pnts'.rjust(w3)+'opp'.rjust(w3)+'tot'.rjust(w3)+'\n')
        lines.append('-'*w+'\n')
        for info in self.part_list:
            lines.append(info[0].ljust(w1)+info[1].ljust(w2)+info[2].rjust(w3)+str(info[3]).rjust(w3)+str(info[4]).rjust(w3)+str(info[5]).rjust(w3)+'\n')
        lines.append('-'*w+'\n')
        lines.append('\n')
        lines.append('\n')
        lines.append('\n')
        
        w=5
        lines.append('-'*w+'\n')
        lines.append('END'.center(w)+'\n')
        lines.append('-'*w+'\n')
        
        return lines

###############
#   3. Main   #
###############

#read data file
fdata=sys.argv[2]
f=open(fdata)
year=f.readline().strip()
fopen=f.readline().strip()
frep=f.readline().strip()
fmem=f.readline().strip()
fplace=f.readline().strip()
finet=f.readline().strip()
fgames=f.readline().strip()
f.close()
players={}

#initialize players with opening balances
#calulate annual depreciation
f=open(fopen)
lines=f.readlines()
for line in lines[1:]:
    info=line.split(',')
    players[info[1].strip('"')]=player(info[1].strip('"'),info[2].strip('"'),int(info[-1]))
f.close()

#calculate representative's depreciation
f=open(frep)
lines=f.readlines()
for line in lines:
	info=line.split(',')
	if players.has_key(info[0]):
		players[info[0]].calc_rep(int(info[1]),int(info[2]),int(info[3]),int(info[4]))
f.close()

#calculate membership points
f=open(fmem)
lines=f.readlines()
for name in lines:
    name=name.strip()
    if players.has_key(name):
        players[name].set_lyom(year)
    else:
        players[name]=player(name,year,0)
    players[name].calc_mem()
f.close()

#calculate SA championship points
f=open(fplace)
lines=f.readlines()
pos=0
qualified=1
qualifiers=[]
others=[]
for line in lines:
    if line.strip()=='*':
        qualified=0
    elif qualified:
        names=line.split(',')
        for name in names:
            name=name.strip()
            if players.has_key(name):
                players[name].calc_place(pos,len(names))
                qualifiers.append(name)
        pos=pos+len(names)
    elif not qualified:
        others.append(line.strip())
for name in set(others)-set(qualifiers):
    if players.has_key(name):
        players[name].calc_place()
f.close()

#calculate internet championship points
f=open(finet)
lines=f.readlines()
pos=0
participants=[]
for line in lines:
    if line.strip()=='*':
        for name in set(players.keys())-set(participants):
            players[name].calc_inet()
        pos=0
        participants=[]
    else:
        names=line.split(',')
        for name in names:
            name=name.strip()
            if players.has_key(name):
                players[name].calc_inet(pos,len(names))
                participants.append(name)
        pos=pos+len(names)
f.close()

#calculate participation points
f=open(fgames)
lines=f.readlines()
for line in lines[1:]:
    info=line.split(',')
    white=info[1]
    black=info[2]
    if players.has_key(white):
        if players.has_key(black):
            players[white].calc_part(info[0],players[black],info[3])
        else:
            players[white].calc_part(info[0],player(black,'',0),info[3])
    if players.has_key(black):
        if players.has_key(white):
            players[black].calc_part(info[0],players[white],info[3])
        else:
            players[black].calc_part(info[0],player(white,'',0),info[3])
f.close()

#calculate closing balances
for name in players.keys():
    players[name].calc_close()
        
#sort players by closing balances
players_list=[]
for name in players.keys():
    players_list.append(players[name])
players_list.sort()
players_list.reverse()

#write results to output files
f=open('wagc_points.txt','w')
f.write('Position,Name,Last year of membership,'+year+' opening balance,Annual depreciation,Representative\'s depreciation,Membership points,SA Championship points,Internet Championship points,Participation points,'+year+' closing balance\n')
pos=1
for playr in players_list:
    f.write(str(pos)+','+str(playr)+'\n')
    print playr
    pos=pos+1
    try:
        g=open('recordsheets'+'/'+playr.name.replace(' ','_')+'.txt','w')
    except IOError:
        os.mkdir('recordsheets')
        g=open('recordsheets'+'/'+playr.name.replace(' ','_')+'.txt','w')
    g.writelines(playr.report())
    g.close()
f.close()
