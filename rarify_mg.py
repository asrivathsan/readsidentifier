import sys
import numpy,fileinput
from collections import Counter
sampling_points= range(0,100,1)
sampling_counter={}
reps=sys.argv[2]
o1=sys.argv[3]
def sample1(f1,f2,f3):
	g1=open(f1)
	g2=open(f2)
	g3=open(f3)
	g1ids={}
	g2ids={}
	g3ids={}
	for each in g1:
		m=each.strip().split('\t')
		g1ids[m[0]]=m[1:]
	for each in g2:
		m=each.strip().split('\t')
		g2ids[m[0]]=m[1:]
	for each in g3:
		m=each.strip().split('\t')
		g3ids[m[0]]=m[1:]

	idlist=g3ids.keys()+g1ids.keys()+g2ids.keys()

	total_n= len(idlist)
	print total_n
	return [g1ids,g2ids,g3ids,total_n,idlist]

lfile=open(sys.argv[1])
inpaths=lfile.readlines()
pars={}
for each in inpaths:
	m=each.split('\t')
	pars[m[0]]=sample1(m[1],m[2],m[3])
	pars[m[0]].append(m[4].strip())


	
outfile_main=open(o1+"_summary",'w')

sample_idlist=[]
for x in sampling_points:
	counter=1
	counts=[]
	while counter<=int(reps):
		sample_reps=[]
		for id in pars.keys():
			try:
				sample_vec=list(numpy.random.choice(pars[id][4],int(float(x)*0.01*float(pars[id][3])), replace=False))
				#		sample_vec = idlist 
				g1subset={}
				g2subset={}
				g3subset={}
				g1ids=pars[id][0]
				g2ids=pars[id][1]
				g3ids=pars[id][2]
				for each in list(set(g1ids.keys())&set(sample_vec)):
					g1subset[each]=g1ids[each]
				for each in list(set(g2ids.keys())&set(sample_vec)):
					g2subset[each]=g2ids[each]
				for each in list(set(g3ids.keys())&set(sample_vec)):
					g3subset[each]=g3ids[each]
				gsub_fg={}
				g1sub_fg={}
				g2sub_fg={}
				g3sub_fg={}
				for fg in g1subset.values():
					if fg[0][0]!="n":
						g1sub_fg[" ".join(fg)]=fg[1]
						gsub_fg[" ".join(fg)]=fg[1]
				for fg in g2subset.values():
					if fg[0][0]!="n":
						g2sub_fg[" ".join(fg)]=fg[1]
						gsub_fg[" ".join(fg)]=fg[1]
				for fg in g3subset.values():
					if fg[0][0]!="n":
						g3sub_fg[" ".join(fg)]=fg[1]
						gsub_fg[" ".join(fg)]=fg[1]
				genids=g1sub_fg.keys()+g2sub_fg.keys()+g3sub_fg.keys()
				genids_counter= Counter(genids)
				genids_accepted={}
				for k in genids_counter.keys():
					if genids_counter[k]>=2:
						genids_accepted[k]=gsub_fg[k]		
				f1sub_fg={}
				f2sub_fg={}
				f3sub_fg={}
				for fg in g1subset.values():
					if fg[1][0]!="n":
						if fg[1] not in genids_accepted.values():
							f1sub_fg[fg[1]]=fg[1]
				for fg in g2subset.values():
					if fg[1][0]!="n":
						if fg[1] not in genids_accepted.values():
							f2sub_fg[fg[1]]=fg[1]
				for fg in g3subset.values():
					if fg[1][0]!="n":
						if fg[1] not in genids_accepted.values():
							f3sub_fg[fg[1]]=fg[1]
				famids=f1sub_fg.keys()+f2sub_fg.keys()+f3sub_fg.keys()
				famids_counter= Counter(famids)
				famids_accepted=[]
				for k in famids_counter.keys():
					if famids_counter[k]>=2:
						famids_accepted.append(k)
				allids_accepted=famids_accepted+genids_accepted.keys()
				sample_reps.append(allids_accepted)
			except ValueError:
				pass
		genids={}
		for each in sample_reps:
			for genfam in each:
				m=genfam.split(" ")
				if len(m)==2:
					genids[genfam]=m[1]
		for each in sample_reps:
			for genfam in each:
				m=genfam.split(" ")
				if len(m)==1:
					if genfam not in genids.values():
						genids[genfam]=genfam
		counter+=1
		counts.append(len(genids))
	avg=numpy.mean(counts)
	std=numpy.std(counts)
	outfile_main.write(sys.argv[3]+"_"+str(x)+'\t'+str(avg)+'\t'+str(std)+'\n')

	
