# /usr/bin/env python

""" 
Convert the raw sqlite similarity data into an smat file that
we can use with Matlab.
"""

import sys
import os
import optparse
import itertools
import time
import operator

import sqlite3

    
class IDer:
    def __init__(self):
        self.curid = 0
        self.str2id = {}
    def get(self, str):
        id = self.str2id.get(str,-1)
        if id == -1:
            id = self.curid
            self.curid += 1
            self.str2id[str] = id
        return id
    def iter_sorted(self):
        return sorted(self.str2id.iteritems(), 
            key=operator.itemgetter(1))
    def size(self):
        return len(self.str2id)

class SmatConverter:
    def __init__(self,file,filename,opts):
        """ 
        @param opts a set of options to configure the converter
          opts.comment = True/False if comments could be in the file
          opts.dups = True/False if there are duplicate edges
          opts.undir = True/False if the edges should be undirected,
            but only one edge is listed
          (Not implemented)
          opts.weights = True/False if the edges have weights
          opts.numeric = True/False if the graph has numeric IDs 
            (Python ints), then we can save memory by storing these.  
        """
        self.names = IDer()
        self.edges = []
        self.opts = opts
        self.file = file
        self.filename = filename
        self.t0 = time.time()
        self.last_time = self.t0
        if opts.filelist:
            self.edges = FileList()
            
        if opts.filelist: assert(opts.dups is False)
        
    def remove_duplicate_edges(self):
        # TODO modify this function
        # to handle weights
        self.edges.sort()
        self.edges = [k for k,v in itertools.groupby(self.edges)]
        
    def report(self,lineno):
        shortname = self.filename[0:min(len(self.filename),15)]
        t = time.time()
        print "%15s %7i nodes %8i edges %5.0f sec."%(
            shortname, self.names.size(), len(self.edges), 
            t - self.t0)
        self.last_time = t
        
    def read_edges(self):
        for lineno,line in enumerate(self.file):
            if self.opts.comment and line[0]=='#':
                continue
            line = line.rstrip()
            parts = line.split()
            if len(parts) == 0:
                continue
            if len(parts) == 1:
                print line
            if self.opts.numeric:
                parts[0] = int(parts[0])
                parts[1] = int(parts[1])
                
            id1 = self.names.get(parts[0])
            id2 = self.names.get(parts[1])
            self.edges.append((id1,id2))
            if self.opts.undir:
                self.edges.append((id2,id1))
                
            if lineno%1000:
                if time.time() - self.last_time > 10.:
                    self.report(lineno)
            
        if self.opts.dups:
            # remove duplicates
            self.remove_duplicate_edges()
    
    def write_edges(self,filename):
        file = open(filename,'wb') # always use unix newliens
        nedges = len(self.edges)
        nverts = self.names.curid
        file.write('%i %i %i\n'%(nverts,nverts,nedges))
        val = 1
        for (i,j) in self.edges:
            file.write('%i %i %i\n'%(i,j,val))
        file.close()
        
    def write_names(self,filename):
        # always use unix newline
        file = open(filename,'wb')
        for namepair in self.names.iter_sorted():
            if self.opts.numeric:
                file.write(str(namepair[0]))
            else:
                file.write(namepair[0])
            file.write('\n')
        file.close()
    
def build_filename(orig,type):
    basename,ignore = os.path.splitext(orig)
    return basename + "." + type
    
def parse_options():
    parser = optparse.OptionParser(usage="test")
    parser.add_option('-u','--undirected_edges',dest='undir',
        default = False, action='store_true',
        help = 'the file only has one undirected edge listed')
    parser.add_option('-c','--comments', dest='comment',
        default=False, action='store_true',
        help = 'the file has comment lines flagged with #')
    parser.add_option('-d','--duplicates',dest='dups',
        default=False, action='store_true',
        help = 'the file has duplicate edges')
    parser.add_option('--names',dest='write_names',
        default=True, action='store_true',
        help = 'output names for each object')
    parser.add_option('--nonames',dest='write_names',
        action='store_false', help='do not output names')
    parser.add_option('--numeric',dest='numeric',default=False,
        action='store_true', help='the names are numeric ids')
    parser.add_option('--filelist',dest='filelist',default=False,
        action='store_true', 
        help='store edges in a set of files for lower memory usage')
    
    
    opts,args = parser.parse_args()
    return (opts,args)
    

def db_as_file():
    simdb = 'artist_similarity.db'
    conn = sqlite3.connect(simdb)
    c = conn.cursor()
    for simpair in c.execute("SELECT * FROM similarity"):
        yield "%s %s"%(simpair[0], simpair[1])
    conn.close()
    
def read_artist_map():
    # read the artistmap into a dictionary
    
    artistfile = 'unique_artists.txt'
    
    amap = {}
    for line in open(artistfile):
        line = line.rstrip()
        parts = line.split('<SEP>')
        aid = parts[0]
        aname = parts[3]
        if aid in amap:
            print >> "weird, %s was listed twice"%(aid)
        amap[aid] = aname
    
    return amap    

def main():
    opts,args = parse_options()    
    
    amap = read_artist_map()
    
    smatc = SmatConverter(db_as_file(), 'artist_similarity.db', opts )
    smatc.read_edges()
    smatc.write_edges("artistsim.smat")
    
    
    
    nfile = open("artistsim.names","wb")
    for namepair in smatc.names.iter_sorted():
        aid = namepair[0]
        if aid not in amap:
            print >> "crap, aid %s not listed in names"%(aid)
        nfile.write(amap[aid])
        nfile.write('\n')
    nfile.close()
    
if __name__=='__main__':
    main()    
    
