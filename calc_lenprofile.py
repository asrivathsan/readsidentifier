import sys,fileinput
o=open(sys.argv[1])

outfile=open(sys.argv[3],'w')
l=o.readlines()
k={}
for each in l:
	m=each.split('\t')
	k[m[0]]=''


n=0
flag=False
for each in fileinput.input([sys.argv[2]]):
	if n%2==0:
		if each.split(" ")[0][1:] in k:
			m=each.split(" ")
			outfile.write(m[0].strip()[1:]+'\t')
			flag=True
	elif n%2==1:
		if flag==True:
			outfile.write(str(len(each.strip()))+'\n')
			flag=False
	n=n+1
o.close()
outfile.close()
