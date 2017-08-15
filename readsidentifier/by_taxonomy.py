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


import fileinput,sys

# Applies the identity threshold
def best_by_id(infile,cutoff):
	outfile=open(infile+'.byid'+cutoff,'w')
	for hit in fileinput.input([infile]):
		if hit!='\n':
			HitValues=hit.split('\t')
			if float(HitValues[2])>=float(cutoff):
				outfile.write(hit)
	outfile.close()
	
# Finds the various parent taxid information for a given taxid
def tax_to_cat(infile,PathToTaxonomy):
	catdict={}
	for line in fileinput.input([PathToTaxonomy+"/nodes.dmp"]):
		DictValues=line.split('\t')
		catdict[DictValues[0]]=DictValues[2]
	outfile=open(infile+'.cat','w')
	dmpfile=open(infile+'.dmp','w')
	for line in fileinput.input([infile]):
		HitValues=line.strip().split('\t')
		TaxID=HitValues[-1]
		try:
			TaxCategories=[]
			n=1
			flag=TaxID
			while n<50:
				if flag!=catdict[flag]:
					TaxCategories.append(catdict[flag])
					flag=catdict[flag]
				if flag==catdict[flag]:
					n=49
				n=n+1
			outfile.write(line.strip())
			for cat in TaxCategories:
				outfile.write('\t'+cat)
			outfile.write('\n')
		except KeyError:
			dmpfile.write(line)
	outfile.close()
	dmpfile.close()
	
# Makes consistancy profiles such based on taxid. Taxid considered are species, genus, family, order, class and phylum
def consist(infile,PathToTaxonomy):
	TargetCategories={}
	outfile=open(infile+".con",'w')
	catdict={}
	for line in fileinput.input([PathToTaxonomy+"/nodes.dmp"]):
		DictValues=line.split('\t')
		catdict[DictValues[0]]=DictValues[4]
	fileinput.close()
	for line in fileinput.input([infile]):
		HitValues=line.strip().split('\t')
		TargetCategories[HitValues[0]]={'perc':HitValues[2],'species':[],'genus':[],'family':[],'order':[],'phylum':[],'class':[],'kingdom':[]}
	fileinput.close()
	for line in fileinput.input([infile]):
		HitValues=line.strip().split('\t')
		n=12
		while n<len(HitValues):
			for cat in TargetCategories[HitValues[0]].keys():
				if catdict[HitValues[n]]==cat:
					if HitValues[n] not in TargetCategories[HitValues[0]][cat]:
						TargetCategories[HitValues[0]][cat].append(HitValues[n])
			n=n+1
	print "Number of ids with taxonomic information:" + str(len(TargetCategories))
	for ID in TargetCategories.keys():
		LCA_per_ID={}
		for cat in TargetCategories[ID].keys():
			if len(TargetCategories[ID][cat])>1:
				LCA_per_ID[cat]=str(','.join(TargetCategories[ID][cat]))
			elif len(TargetCategories[ID][cat])==0:
				LCA_per_ID[cat]='n'+str(len(TargetCategories[ID][cat]))
			else:
				LCA_per_ID[cat]=TargetCategories[ID][cat][0]
		outfile.write(ID+'\t'+TargetCategories[ID]['perc']+'\t'+LCA_per_ID['species']+'\t'+LCA_per_ID['genus']+'\t'+LCA_per_ID['family']+'\t'+LCA_per_ID['order']+'\t'+LCA_per_ID['class']+'\t'+LCA_per_ID['phylum']+'\t'+LCA_per_ID['kingdom']+'\n')
	outfile.close()

# convert taxid information to scienctific names
def cat_to_name(infile,PathToTaxonomy,suffix):
	namesdict={}
	for line in fileinput.input([PathToTaxonomy+"/names.dmp"]):
		DictValues=line.split('\t')
		if DictValues[6]=="scientific name":
			namesdict[DictValues[0]]=DictValues[2]
	outfile=open(suffix,'w')
	for line in fileinput.input([infile]):
		HitValues=line.strip().split('\t')
		n=2
		IDValues=[HitValues[0],HitValues[1]]
		while n<9:
			try:
				IDValues.append(namesdict[HitValues[n]])
			except KeyError:
				try:
					newlist=[]
					for each in HitValues[n].split(','):
						newlist.append(namesdict[each])
					IDValues.append(",".join(newlist))
				except KeyError:
					IDValues.append(HitValues[n])
			n=n+1
		for value in IDValues:
			outfile.write(value+'\t')
		outfile.write('\n')
	outfile.close()
