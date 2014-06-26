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

import fileinput,os,sys
def matchdb(infile,db,PathToDB):
	gidict={}
	# Dictionary containing keys: ginumber and values: taxid
	DBname=PathToDB+"/"+db
	n=1
	for line in fileinput.input([DBname]):
		if len(line)>2:
			try:
				DictValues=line.strip().split('\t')
				gidict[DictValues[0]]=DictValues[1]
			except KeyError:
				print "error in database file "+DBname+" line "+n
				print "Bypassing this line"
				pass
		n=n+1
	outfile=open(infile+".withgi",'w')
	fileinput.close()
	for line in fileinput.input([infile]):
		HitValues=line.split('\t')
		TrimmedLine=line[:-1]
		if "|" in HitValues[1]:
			GI=HitValues[1].split('|')
			ginumber=GI[1].split(':')
			try:
				outfile.write(TrimmedLine+'\t'+gidict[ginumber[0]]+'\n')
			except KeyError:
				pass
				# parses any blast output line that contains the gi number
		elif len(HitValues[1])>2:
			try:
				outfile.write(TrimmedLine+'\t'+gidict[HitValues[1]]+'\n')
			except KeyError:
				pass
				# if the database contains sequences other than the genbank sequences, the entire id would be used (as these sequence headers do not obey the gi|123234|xx format). However a file similar to gi_taxid_nucl.dmp needs to be created with SequenceID<tab>TaxonID<RETURN> and the file stored in PathToDB., ensure sequenceID has no space, or give values before space are taken into consideration by BLAST.
	outfile.close()
	fileinput.close()

def dmp(infile):
	infileids={}
	for line in fileinput.input([infile]):
		infileids[line.split('\t')[0]]=line
	fileinput.close()
	outfile=infile+".withgi"
	outfileids={}
	for line in fileinput.input([outfile]):
		outfileids[line.split('\t')[0]]=''
	fileinput.close()
	DmpHits=list(set(infileids.keys())-set(outfileids.keys()))
	print "Unable to find taxid for "+str(len(DmpHits))+" reads"
	dmpfile=open(outfile+".dmp",'w')
	for ID in DmpHits:
		dmpfile.write(infileids[ID])

