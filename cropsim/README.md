Crop similarity graphs based on HarvestChoice
=============================================

The following graphs are 25 nearest neighbor graphs built from the harvested area and yield from the spatial production allocation model of crop production. See <mapspam.info> for more information.

At a high level, for each pixel in the world, we have an estimate of how much of 48 crops are grown (or a slightly smaller set in earlier version of the data). We will draw a relationship between two pixels if they have similar crop profiles as determined by Euclidean distance. This is about the most basic thing you could do.

High level graph information
----------------------------
There are 6 graphs based on 6 different datasets:

* 2000 - harvestarea
* 2000 - yield
* 2005 - harvestarea
* 2005 - yield
* 2010 - harvestarea
* 2010 - yield

Each node is connected to its 25 nearest neighbors based on Euclidean distance to other pixels that have the closest crop profiles. 

The 2000 data is based on the following 20 crops:    
      wheat,rice,maize,barley,millet,sorgum,potato,swpy,casswary,banp,soybean,bean,opul,sugarcane,sugarbeat,coffee,cotton,ofib,grou,ooil,othe
The 2005 data is based on the following 42 crops
      :whea_a, :rice_a, :maiz_a, :barl_a, :pmil_a, :smil_a, :sorg_a, :ocer_a, :pota_a, :swpo_a, :yams_a, :cass_a, :orts_a, :bean_a, :chic_a, :cowp_a, :pige_a, :lent_a, :opul_a, :soyb_a, :grou_a, :cnut_a, :oilp_a, :sunf_a, :rape_a, :sesa_a, :ooil_a, :sugc_a, :sugb_a, :cott_a, :ofib_a, :acof_a, :rcof_a, :coco_a, :teas_a, :toba_a, :bana_a, :plnt_a, :trof_a, :temf_a, :vege_a, :rest_a
The 2010 data is based on the following 49 crops



Usage and citation information
------------------------------
We cite the data as follows

> Any and all derived products (e.g., tables, figures, maps) generated
> using this data must be given due attribution according to the suggested
> citation supplied:
> You, L., U. Wood-Sichra, S. Fritz, Z. Guo, L. See, and J. Koo. 2014.
> Spatial Production Allocation Model (SPAM) 2010 V1r1. [October 8, 2019].
> Available from http://mapspam.info and on IFPRI’s Dataverse Site.

and provide the following Bibtex reference

```
@misc{You-2019-spam,
  title = {Spatial Production Allocation Model ({SPAM}) 2010 {V1r1}},
  year = {2014},
  author = {You, L. and  U. Wood-Sichra and S. Fritz and Z. Guo and L. See and J. Koo}
  note = {October 8, 2019 release. Available from \url{http://mapspam.info}
    and on Harvard's Dataverse Site.},
}

Getting the raw data
---------------------
This data is available at Harvard Dataverse

2010 - <https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/PRFF8V>
2005 - <https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DHXBJX>
2000 - <https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/A50I2T>

For each release, we downloaded the yield and harvested area CSV files.

    MD5 (spam2000v3.0.7_global_harvested-area.dbf-csv.zip) = 46c29b114e7c388e53f5333590669c83
    MD5 (spam2000v3.0.7_global_yield.dbf-csv.zip) = 1fcd389a288d5a53471b24d826853d1b
    MD5 (spam2005v3r2_global_harv_area.csv.zip) = 1da269a0ff7b9e7f7407866feee5dc8f
    MD5 (spam2005v3r2_global_yield.csv.zip) = 12693294f87c0e17544f23f3b013f342
    MD5 (spam2010v1r1_global_harv_area.csv.zip) = f4dc02e5b07348e292d3ebea67fc0590
    MD5 (spam2010v1r1_global_yield.csv.zip) = 316f8c76b17c820fd89dc75bd50ae079

Then, we unzipped them to a directory (in my Downloads directory, hence the datadir
    in the processing script.)

The 2005 files did not contain the xy coordinates of each cell,
so we needed to add those.

It turns out CELL5M is a very simple format.
There are 4320 longitude buckets and 2160 latitude buckets
Each bucket is 0.08333333333333333. The following Julia routine will
convert from cell5m to latlong and this matches the cell5m data to Float64
precision.

        function cell5m_to_latlong(cell::Int)
          nrows = 4320
          ncols = 2160
          col, row = divrem(cell, nrows)
          x = row*0.0833333333333333333-(180-0.0833333333333333333/2)
          y = (90-0.0833333333333333333/2) - col*0.0833333333333333333
          return x,y
        end






Processing the files
--------------------
`parse_network.jl`  This will produce all of the output. It takes a while
becaus we use a very primitive nearest neighbor computation.
