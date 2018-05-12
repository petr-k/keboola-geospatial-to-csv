# keboola-geospatial-to-csv

A Keboola Connection processor component that can produce CSV tables from various geospatial formats.

## Data formats
Input files can be one the supported formats:
* shapefile
* KML

Output files are CSVs with a geometry column and optionally additional
nonspatial fields present in the data source.

The geometry column in the output CSV can be formatted as one of:
* _GeoJSON feature_
* _GeoJSON geometry_
* _WKT_
