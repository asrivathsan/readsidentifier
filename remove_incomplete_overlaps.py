#scripts that uses output of calclenprof.py to exclude reads from blastoutput that have incomplete overlaps. usage is python remove_incomplete_overlaps.py blastoutfile lenprofilefile 
import sys,math,fileinput
o=open(sys.argv[1])
l=o.readlines()
outfile=open(sys.argv[1]+"labelled",'w')
qlen={}
slen={}
for each in fileinput.input([sys.argv[2]]):
	m=each.split('\t')
	qlen[m[0]]=int(m[1].strip())
fileinput.close()

for each in l:
	m=each.split('\t')
	if float(m[2])>98 and int(m[3])>49:
		if math.fabs(int(m[7])-int(m[6])+1) < qlen[m[0]]:
			pass
		else:
			outfile.write(each)

outfile.close()
fileinput.close()
