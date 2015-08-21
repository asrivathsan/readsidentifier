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

import fileinput

def parse(InFileName,LengthCutoff):
	PassedHits=[] 

	# Hits that meet the overlap requirement
	for line in fileinput.input([InFileName]):
		if line!='\n':
			HitValues=line.split('\t')
			if int(HitValues[3])>int(LengthCutoff):
				PassedHits.append(line)
			
	fileinput.close()
	IdsWithHits={} 

	# Dictionary of unique ids that meet the overlap requirement
	for hit in PassedHits:
		HitValues=hit.split('\t')
		IdsWithHits[HitValues[0]]=[]

	for hit in PassedHits:
		HitValues=hit.split('\t')
		IdsWithHits[HitValues[0]].append(hit)
	
	FilteredHits={} 
	# Dictionary of unique ids such that the hit with best ID is retained.

	for ID in IdsWithHits.keys():
		FilteredHits[ID]=[]

	for ID in IdsWithHits.keys():
		IDsublist=[]
		for hit in IdsWithHits[ID]:
			HitValues=hit.split('\t')
			ScoreToSubject=HitValues[11]
			Score=ScoreToSubject.strip()
			IDsublist.append(int(ScoreToSubject))
		BestScore=max(IDsublist)
		for hit in IdsWithHits[ID]:
			HitValues=hit.split('\t')
			ScoreToSubject=HitValues[11]
			ScoreToSubject=ScoreToSubject.replace('\n','')
			if BestScore==float(ScoreToSubject):
				FilteredHits[ID].append(hit)


	outfile=open(InFileName+".parsed.lencutoff"+LengthCutoff,'w')

	for ID in FilteredHits.keys():
		for hit in FilteredHits[ID]:
			outfile.write(hit)

	outfile.close()
