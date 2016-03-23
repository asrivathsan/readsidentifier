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
for each in fileinput.input([sys.argv[3]]):
	m=each.split('\t')
	slen[m[0]]=int(m[1].strip())

for each in l:
	m=each.split('\t')
	if float(m[2])>98 and int(m[3])>49:
		if math.fabs(int(m[7])-int(m[6])+1) < qlen[m[0]]:
			if min([int(m[8]),int(m[9])]) ==1 or max([int(m[8]),int(m[9])])>=slen[m[1]]:
				pass
			else:
				pass
		else:
			outfile.write(each)

outfile.close()
fileinput.close()
