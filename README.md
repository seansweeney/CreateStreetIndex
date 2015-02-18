## CreateStreetIndex
This is a quick-and-dirty ArcPy script to create a street index from a grid index and road centerline feature class.

The script simply runs the Intersect geoprocessing tool to split the centerlines by grid and attach the grid name to the resulting street segments.  It then sorts the resulting street list and the corresponding grid(s) list, and creates an output text file containing these lists separated by a a tab stop.  Letter headings are also output when the first letter of the street name changes.  The output looks like the following:

> A  
> Aberdeen Ave	E-2, F-2  
> Aberdeen Ct	F-2  
> ..  
> Avon Pl	D-4  
> Avon St	D-4, E-4  
> B  
> Bailey Pl	I-5  
> Ballord Pl	H-5  
> ...  
> Buena Vista Pk	C-4, D-4  
> Burns Ct	F-3, F-4  
> C  
> Cadbury Rd	D-3  
> Callender St	H-5  
> ...  

## Running the script
The script takes five inputs:
```powershell  
CreateStreetIndex <centerline_feature_class> <centerline_street_name> <index_feature_class> <index_name> <output_file>
```

* *centerline_feature_class* : full path to the centerline feature class
* *centerline_street_name* : name of the field in the centerline feature class that will be output to the file (i.e. 'Aberdeen Ave')
* *index_feature_class* : full path to the index grid feature class
* *index_name* : name of the field in the index grid feature class that will be output to the file (i.e. 'E-2, F-2')
* *output_file* : full path to the output file

Here's an example:

```powershell  
CreateStreetIndex "//data/sde/mydb.sde/db.schema.Centerline" "Street_Name" "//data/shp/AtlasGrid.shp" "GRID_ID" "C:/temp/street_index.txt"
```