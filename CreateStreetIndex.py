import os
from collections import defaultdict
from collections import OrderedDict
import arcpy

def main(argv=None):
    if len(argv) != 5:
        arcpy.AddMessage("Usage: CreateStreetIndex <centerline_feature_class> <centerline_street_name> <index_feature_class> <index_name> <output_file>")
        return

    (road_centerlines, street_name , index_map, index_name, output_file) = tuple(argv)

    arcpy.env.overwriteOutput = True
    scratch_workspace =  arcpy.env.scratchGDB

    # Select all features from map index that don't have NULL names
    index_map_layer = arcpy.management.MakeFeatureLayer(index_map, 'indexmap',
                                                   """{0} IS NOT NULL""".format(index_name))

    # Make sure we have some features to work with
    cnt = arcpy.management.GetCount(index_map_layer)
    if not int(cnt.getOutput(0)) > 0:
        arcpy.AddError('{0} field contains all NULL values and cannot proceed.'.format(index_name))
        return

    # Intersect centerlines with the map index features.
    arcpy.AddMessage('--Intersecting centerlines with index layer...')
    intersect_result = arcpy.analysis.Intersect([road_centerlines, index_map_layer], os.path.join(scratch_workspace, 'centerlines_index'), output_type='LINE')

    # Make a view of the intersect result where street name is not null.
    result_view = arcpy.management.MakeTableView(intersect_result,  'result_view',
                                             """{0} IS NOT NULL AND {0} <> ''""".format(street_name ))


    # Create a defaultdict for the streets so they can be sorted by key
    streets = defaultdict(list)

    # Fields to output
    fields = [street_name , index_name]

    # Loop through the view and get a list of index values for each street
    with arcpy.da.SearchCursor(result_view, fields) as rows:
        for row in rows:
            s = row[0]  # street name
            p = row[1]  # page number

            streets[s].append(p)

    # Now that we have a full list, sort by street name
    sortedstreets = OrderedDict(sorted(streets.items()))

    # Loop through the sorted streets and create output
    firstletter = ''
    f = open(output_file, 'w')
    for street, indexes in sortedstreets.iteritems():
        if street[0] != firstletter:
            firstletter = street[0]
            f.write(firstletter + '\n')
        output_string = street + "\t" + ', '.join(sorted(set(indexes))) + '\n'
        f.write(output_string)

    f.close()

#    # Delete intermediate data.
    arcpy.AddMessage('--Cleaning up intermediate data...')
    arcpy.management.Delete(intersect_result)
## End main function

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))