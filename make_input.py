###############################
#                             #
#	make_input.py             #
#	Reinhardt Messerschmidt   #
#	2006-10-22                #
#                             #
###############################

import sys

year=sys.argv[1]
filename=sys.argv[2]

#read the games from the input file and make some format changes
infile=open(filename)
outfile=open('games.txt','w')
inlines=infile.readlines()
outlines=[]
count=0
for inline in inlines:
    info=inline.split(',')
    if info[6]<>'0':
        date=info[0].strip('"').split('/')
        black=info[1].strip('"')
        white=info[2].strip('"')
        stones=info[3]
        komi=info[4]
        if info[6]=='0.5':
            type='i'
        elif info[6]=='1':
            type='c'
        elif info[6]=='1.5':
            type='t'
        try:
                result=info[7].strip('"').lower()
                outline=date[2]+date[1]+date[0]+','+white+','+black+','+type+','+stones+','+komi+','+result+'\n'
        except:
            print info
            print "LINENO:" + str(count)
            raise
        count +=1
        outlines.append(outline)
    
outfile.write('Date,White,Black,Type,Number of stones placed by Black with 1st move,Komi,Result\n')
          
#sort the games by date and write them to the output file
for month in range(1,13):
    for day in range(1,32):
        remaining_outlines=[]
        for line in outlines:
            if line[0:8]==year+`month`.rjust(2,'0')+`day`.rjust(2,'0'):
                outfile.write(line)
            else:
                remaining_outlines.append(line)
        outlines=remaining_outlines

infile.close()
outfile.close()
