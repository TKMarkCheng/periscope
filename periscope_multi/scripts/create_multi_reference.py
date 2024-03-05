from periscope_multi import __version__
from BCBio import GFF
import pysam
import argparse

def main(args):
    print(args)
    a=''.join(open(args.fasta,'r').readlines()[1:]).replace('\n','')
    b=open('multi_ref.faa','w')
    in_file = args.gff_file
    in_handle = open(in_file)
    ab= GFF.parse(in_handle)
    end=None
    begin=None
    search = str(args.leader)
    for rec in ab:
        for feature in rec.features:
            if feature.type=='gene':
                end=feature.location.nofuzzy_end
                b.write('>')
                b.write(str(feature.qualifiers['Name'][0]))
                b.write('\n')
                if begin !=None:
                    if begin>feature.location.nofuzzy_start:
                        begin=feature.location.nofuzzy_start
                    b.write(search+a[int(begin)-4:min(int(end)+400,len(a))])
                else:
                    b.write(a[0:int(end)+400])
                b.write('\n')
                begin=feature.location.nofuzzy_end
    in_handle.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='make multi_ref')
    parser.add_argument('--fasta', help='reference file',default="The reference file of the specie of interest")
    parser.add_argument('--gff',dest='gff_file',help="gff file with all gene position")
    parser.add_argument('--leader', help='leader sequence to be searched', default="AACCAACTTTCGATCTCTTGTAGATCTGTTCT")


    args = parser.parse_args()
    # args.fasta='periscope/resources/nCoV-2019.reference.fasta'
    # args.gff_file='../../sgENERATE/sgENERATE/recource/script/covid.gff'

    periscope = main(args)