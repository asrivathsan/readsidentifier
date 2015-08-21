# Copyright 2014 Amrita Srivathsan

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import sys,fileinput
def consistpe(inputfile1,inputfile2,PathToDB,outfile):
	DictEnd1={}
	DictEnd2={}
	outfile=open(outfile,'w')
	catdict={}
	for line in fileinput.input([PathToDB+"/nodes.dmp"]):
		DictValues=line.strip().split('\t')
		catdict[DictValues[0]]=DictValues[4]
	for line in fileinput.input([inputfile1]):
		HitValues=line.strip().split('\t')
		DictEnd1[HitValues[0]]={'species':[],'genus':[],'family':[],'order':[],'phylum':[],'class':[],'division':[]}
	fileinput.close()
	for line in fileinput.input([inputfile2]):
		HitValues=line.strip().split('\t')
		DictEnd2[HitValues[0]]={'species':[],'genus':[],'family':[],'order':[],'phylum':[],'class':[],'division':[]}
	fileinput.close()
	for line in fileinput.input([inputfile1]):
		HitValues=line.strip().split('\t')
		n=12
		while n<len(HitValues):
			for ID in DictEnd1[HitValues[0]].keys():
				if catdict[HitValues[n]]==ID:
					if HitValues[n] not in DictEnd1[HitValues[0]][ID]:
						DictEnd1[HitValues[0]][ID].append(HitValues[n])
			n=n+1
	fileinput.close()
	for line in fileinput.input([inputfile2]):
		HitValues=line.strip().split('\t')
		n=12
		while n<len(HitValues):
			for ID in DictEnd2[HitValues[0]].keys():
				if catdict[HitValues[n]]==ID:
					if HitValues[n] not in DictEnd2[HitValues[0]][ID]:
						DictEnd2[HitValues[0]][ID].append(HitValues[n])
			n=n+1
	DictBothEnds={}
	for ID in DictEnd1.keys():
		if ID in DictEnd2.keys():
			DictBothEnds[ID]={'species':[],'genus':[],'family':[],'order':[],'phylum':[],'class':[],'division':[]}
	for ID in DictBothEnds.keys():
		for cat in DictEnd1[ID].keys():
			DictBothEnds[ID][cat]=list(set(DictEnd1[ID][cat])&set(DictEnd2[ID][cat]))
	for ID in DictBothEnds.keys():
		LCA_per_ID={}
		for cat in DictBothEnds[ID].keys():
			if len(DictBothEnds[ID][cat])>1:
				LCA_per_ID[cat]=str(','.join(DictBothEnds[ID][cat]))
			elif len(DictBothEnds[ID][cat])==0:
				LCA_per_ID[cat]='n'+str(len(DictBothEnds[ID][cat]))
			else:
				LCA_per_ID[cat]=DictBothEnds[ID][cat][0]
		outfile.write(ID+'\t'+LCA_per_ID['species']+'\t'+LCA_per_ID['genus']+'\t'+LCA_per_ID['family']+'\t'+LCA_per_ID['order']+'\t'+LCA_per_ID['class']+'\t'+LCA_per_ID['phylum']+'\t'+LCA_per_ID['division']+'\n')

def cat_to_name(infile,PathToDB):
	namesdict={}
	for each in fileinput.input([PathToDB+"/names.dmp"]):
		DictValues=each.split('\t')
		if DictValues[6]=="scientific name":
			namesdict[DictValues[0]]=DictValues[2]

	outfile=open(infile+".final",'w')
	for line in fileinput.input([infile]):
		IDValues=line.strip().split('\t')
		n=1
		Ls_per_ID=[IDValues[0]]
		while n<8:
			try:
				Ls_per_ID.append(namesdict[IDValues[n]])
			except KeyError:
				try:
					newlist=[]
					for each in IDValues[n].split(','):
						newlist.append(namesdict[each])
					Ls_per_ID.append(",".join(newlist))
				except KeyError:
					Ls_per_ID.append(IDValues[n])
			n=n+1
		for value in Ls_per_ID:
			outfile.write(value+'\t')
		outfile.write('\n')

