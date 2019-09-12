# More graph datasets
This purpose of this repository is to collect and distribute more graph datasets from a variety of sources.

For each graph dataset, we'll have a brief description, along with code to generate that data from the primary source. For the moment, we ask you to please cite

    @misc{more-graphs,
      title = "More graph datasets",
      author = "Hopefully many contributors",
      howpublished = "Github: dgleich/more-graphs",
      note = "Accessed on",
    }      

## Other graph repositories
* SuiteSparse Matrix Collection: https://sparse.tamu.edu/
* Colorado Index of Complex Networks: https://icon.colorado.edu/
* Koblenz Network Collection: http://konect.uni-koblenz.de/
* Stanford Network Analysis Project: http://snap.stanford.edu

## File formats

The graph and network data is distributed as an SMAT file.  The format of the file is:

File: Header Body
Header: num_nodes:Int num_nodes:Int num_edges:Int
Body: Edge*num_edges
Edge: source_id:Int dest_id:Int weight:Double

Undirected edges are listed twice, i.e. both (src,dst) and (dst,src)
edges exist.

The node and edge ids run from 0 to num_nodes-1

Example
-------

The following lines describe a 3-node clique in SMAT.

    3 3 6
    0 1 1
    0 2 1
    1 2 1
    1 0 1
    2 0 1
    2 1 1

Various other data are stored as bipartite or weighted graphs. Here is an example:

    3 4 6
    0 0 1.5
    1 1 0.5
    2 2 1
    0 1 0.5
    0 4 1
    2 1 0.5
    
Julia code to read the file
---------------------------



Python code to read the file
----------------------------

The Python code takes in a filename, and returns a list of lists 
representation of the graph.


    def read_smat(filename, set_undirected = True):
        """ Load an SMAT file into a list-of-lists graph representation. """
        f = open(filename, 'rU')
        hdr = f.readline()
        parts = hdr.split()
        nverts = int(parts[0])
        ncols = int(parts[1])
        nedges = int(parts[2])
        nremedges = nedges # number of remaining edges
        if nverts != ncols:
            raise ValueError(
                'read_smat line 1: requires nrows (%i) = ncols (%i) for graph'%(
                nverts, ncols))
        graph = [ [] for _ in xrange(nverts) ]
        for lineno, line in enumerate(f):
            parts = line.split()
            if len(parts) == 0: continue
            if nremedges==0: 
                raise ValueError(
                    'read_smat line %i: more than %i edges found'%(
                    lineno+2, nedges))
            src = int(parts[0])
            dst = int(parts[1])
            if src < 0 or src >= nverts or dst < 0 or dst >= nverts:
                raise ValueError(
                    'read_smat line %i: out-of-range edge (%i,%i) found (nverts=%i)'%(
                    lineno+2, src, dst, nverts))
            graph[src].append(dst)
            nremedges -= 1
        
        return graph

Matlab code to read the file
----------------------------

The following matlab code reads an SMAT file to a Matlab sparse
matrix.

    function A = readSMAT(filename)
    % READSMAT Load a graph into a Matlab sparse matrix
    %   A = readSMAT(filename) where
    %   filename is the name of the SMAT file and
    %   A is the MATLAB sparse matrix

    if ~exist(filename,'file')
        error('readSMAT:fileNotFound', 'Unable to read file %s', filename);
    end

    s = load(filename,'-ascii');
    m = s(1,1);
    n = s(1,2);
    
    ind_i = s(2:length(s),1)+1;
    ind_j = s(2:length(s),2)+1;
    val = s(2:length(s),3);
    clear s;
    A = sparse(ind_i,ind_j,val, m, n);
