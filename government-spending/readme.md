# Data Description 
The data we used is publicly available from [https://www.usaspending.gov/#/download_center/award_data_archive](https://www.usaspending.gov/#/download_center/award_data_archive) for the 2018 fiscal year contracts data. We build a bipartite graph between the funding government sub-agencies and the companies they awarded contracts to. We use the parent company unless it is not stated, in which case we simply use the recipient information.

#### Copyright Info
Please see [https://www.usaspending.gov/#/db_info](https://www.usaspending.gov/#/db_info) on permissible use of D&B data.

# Files
* subagencies.labels
    * file that contains both the agency and subagency name in the format 'agency||subagency'. The agency and subagency at index j has node label j. Note that indices begin from 0
*  companies.labels
    *	this file contains the name of the parent company (if it was given) or the recipient name if the parent name was not given. The name at index j corresponds to node label len(subagencies)+j = 295+j. Note that indices begin at 0.
* contracts-edges.smat
    * An .smat representation of the bipartite graph. One portion represents the government subagencies and the other the companies they contracted in fiscal year 2018.

### Example
The presence of edge (39777, 25) represents that 'DEPARTMENT OF VETERANS AFFAIRS (VA)||VETERANS AFFAIRS, DEPARTMENT OF' (node 25) had a contract with 'BIOSANTE PHARMACEUTICALS  INC.' during the 2018 fiscal year.