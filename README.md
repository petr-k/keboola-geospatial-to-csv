# keboola-geospatial-to-csv

A Keboola component that can produce CSV tables from various geospatial formats.

## Input

File in one of the supported formats:
* shapefile
* KML

## Output

CSV table with a geometry column and optionally additional nonspatial fields present in the data source.

Format of the geometry column in the output CSV can be one of:
* _GeoJSON feature_
* _GeoJSON geometry_
* _WKT_
