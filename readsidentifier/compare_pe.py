# readsidentifier: a pipeline for BLAST based read identifications

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

# Contact: asrivathsan@gmail.com




import fileinput, sys, os
import readsidentifier.by_taxonomy as bt
import readsidentifier.parse_by_ID as parse_by_ID
import readsidentifier.parse_by_score as parse_by_score
import readsidentifier.match_GiToTaxID as match_GiToTaxID
import readsidentifier.compare_pe as compare_pe


infile=open(sys.argv[1])
InputValuesDict={}
for line in infile.readlines():
	if line[0]!='#':
		if len(line.strip())>2:
			InputValues=line.strip().split("=")
			InputValuesDict[InputValues[0]]=InputValues[1].strip().replace(' ','')

prefix=InputValuesDict["outputfileprefix"]
print "results will be stored in .final file"
idcutoff=InputValuesDict['identity']
print "Setting Identity threshold as: " + str(idcutoff)
lencutoff=InputValuesDict['lencutoff']
print "Setting hit length threshold as: " + str(lencutoff)
PathToDB=InputValuesDict['PathToGiTaxid']
print "Setting path to gi_tax directory as: " + str(PathToDB)
PathToTaxonomy=InputValuesDict['PathToTaxonomy']
print "Setting path to Taxonomy directory as: " + str(PathToTaxonomy)
dblist=os.listdir(PathToDB)
print "There are " + str(len(dblist))+" files in gi_tax folder"
Type=InputValuesDict["Type"]
GiTaxIDopt=InputValuesDict['GiTaxIDopt']
ParseMethod=InputValuesDict['ParseMethod']
blastout1=InputValuesDict['blastout1']

if Type=="s":
	print "Processing as single end data"
	print "Setting blastoutput file as:" + str(blastout1)

if Type=="p":
	try:
		blastout2=InputValuesDict["blastout2"]
		print "Processing as paired end data"
		print "Setting blastoutput end1 file as:" + str(blastout1)
		print "Setting blastoutput end2 file as:" + str(blastout2)
	except KeyError:
		print "check config file"


def mastertax(inputfile):
	if GiTaxIDopt=='y':
		print "matching gi to taxid... this may take a while..."
		for db in dblist:
			print db
			match_GiToTaxID.matchdb(inputfile,db,PathToDB)
			print "matched gi to taxid. Now parsing output by length..." 
	elif GiTaxIDopt=='n':
		os.system("cp "+inputfile+ " " +inputfile+".withtaxid")
	if ParseMethod=='score':
		print "parsing blastoutput by length and score
		parse_by_score.parse(inputfile+".withtaxid",lencutoff)
	elif ParseMethod=='identity':
		print "parsing blastoutput by length and identity
		parse_by_ID.parse(inputfile+".withtaxid",lencutoff)
	print "creating taxonomy profile" 
	bt.best_by_id(inputfile+".withtaxid.parsed.lencutoff"+lencutoff,idcutoff)
	bt.tax_to_cat(inputfile+".withtaxid.parsed.lencutoff"+lencutoff+'.byid'+idcutoff,PathToTaxonomy)
	bt.consist(inputfile+".withtaxid.parsed.lencutoff"+lencutoff+'.byid'+idcutoff+'.cat',PathToTaxonomy)
	if Type=='s':
		bt.cat_to_name(inputfile+".withtaxid.parsed.lencutoff"+lencutoff+'.byid'+idcutoff+'.cat.con',PathToTaxonomy,prefix+".final")
	if Type=='p':
		bt.cat_to_name(inputfile+".withtaxid.parsed.lencutoff"+lencutoff+'.byid'+idcutoff+'.cat.con',PathToTaxonomy,inputfile+".withtaxid.parsed.lencutoff"+lencutoff+'.byid'+idcutoff+'.cat.con.final')

mastertax(blastout1)

if Type=='p':
	print "Processing end 2"
	mastertax(blastout2)
	print "comparing end 1 and end 2"
	compare_pe.consistpe(blastout1+".withtaxid.parsed.lencutoff"+lencutoff+'.byid'+idcutoff+'.cat',blastout2+".withtaxid.parsed.lencutoff"+lencutoff+'.byid'+idcutoff+'.cat',PathToTaxonomy, prefix)
	compare_pe.cat_to_name(prefix,PathToTaxonomy)
