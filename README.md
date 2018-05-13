# keboola-geospatial-to-csv
[![Build Status](https://travis-ci.org/petr-k/keboola-geospatial-to-csv.svg?branch=master)](https://travis-ci.org/petr-k/keboola-geospatial-to-csv)

A [Keboola Connection](https://www.keboola.com/product) component (more specifically a [processor](https://developers.keboola.com/extend/component/processors/)) that converts data in various geospatial formats into CSV tables. It is based on [GDAL (Geospatial Data Abstraction Library)](http://www.gdal.org/).

## Data formats
Input files can be in one the supported formats:
* [ESRI Shapefile](https://en.wikipedia.org/wiki/Shapefile)
* [KML](https://en.wikipedia.org/wiki/Keyhole_Markup_Language)
* [GeoJSON](https://en.wikipedia.org/wiki/GeoJSON) feature collection

Output files are CSVs with a geometry column and optionally additional
nonspatial fields present in the data source.

The geometry column in the output CSV can be formatted as one of:
* _GeoJSON feature_
* _GeoJSON geometry_
* [_Well-known text (WKT)_](https://en.wikipedia.org/wiki/Well-known_text) geometry

### Example conversion
For instance, a GeoJSON feature collection document such as this:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "Van Dorn Street",
        "marker-color": "#0000ff",
        "marker-symbol": "rail-metro",
        "line": "blue"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [
          -77.12911152370515,
          38.79930767201779
        ]
      }
    }
  ]
}
```

would produce the following CSV:

```csv
geojson_geometry,name,marker-color,marker-symbol,line
"{ ""type"": ""Point"", ""coordinates"": [ -77.129111523705149, 38.79930767201779 ] }",Van Dorn Street,#0000ff,rail-metro,blue
```

The above is a result of using the default configuration, which formats the geometry as GeoJSON. However, you could configure the processor so that geometry is encoded differently, e.g. using WKT:

```csv
wkt_geometry,name,marker-color,marker-symbol,line
POINT (-77.129111523705149 38.79930767201779),Van Dorn Street,#0000ff,rail-metro,blue
```

In other words, there's no strict relationship between the format of the source geospatial file and the way geometry is represented in the resulting CSVs; you can easily mix and match. See [Configuration](#configuration) for more details.

## Usage

`keboola-geospatial-to-csv` is a KBC processor. As the [documentation on processors](https://developers.keboola.com/extend/component/processors/) states:

> Processors are additional components which may be used before or after running an arbitrary component (extractor, writer, etc.).

You will, however, most likely want to use this processor *after* an *extractor*. For instance, when using the Keboola S3 extractor component, you can add `keboola-geospatial-to-csv` as the first processor in the processor chain, so that geospatial datafiles are converted to CSVs as part of your extractor setup.

### How it works
`keboola-geospatial-to-csv` will walk the input files and, by default, try to convert any supported geospatial data files, (as recognized by their extensions) into CSV. You can configure which formats and filename patterns will be processed, but the default configuration will work perfectly fine for majority of use cases.

#### Mapping of input files to output files
Output files will mirror the directory structure of the input files, e.g.:

| Example input file      | Output file             |
|-------------------------|-------------------------|
| stations.kml            | stations.csv            |
| shapefiles/stations.shp | shapefiles/stations.csv |


#### Example processor configuration
The following example show how you would use this processor in tandem with Keboola's _S3 Simple Storage extractor_.

First, you would set up a new S3 extractor as usual. When editing the extractor configuration, switch to _JSON editor mode_ and add this processor as the very first `processors.after` item:

```json
{
  "parameters": {
    "bucket": "petr-k-test-bucket",
    "key": "spatial-data/*",
    "includeSubfolders": true,
    "newFilesOnly": false
  },
  "processors": {
    "after": [
      {
        "definition": {
          "component": "petr-krebs.app-geospatial-to-csv"
        },
        "parameters": {}
      },
      {
        "definition": {
          "component": "keboola.processor-move-files"
        },
        "parameters": {
          "direction": "tables",
          "addCsvSuffix": false
        }
      },
      {
        "definition": {
          "component": "keboola.processor-create-manifest"
        },
        "parameters": {
          "delimiter": ",",
          "enclosure": "\"",
          "incremental": false,
          "primary_key": [],
          "columns": [],
          "columns_from": "header"
        }
      },
      {
        "definition": {
          "component": "keboola.processor-skip-lines"
        },
        "parameters": {
          "lines": 1
        }
      }
    ]
  }
}
```

Looking at the above, note that:
* The _component id_ for this processor is `petr-krebs.app-geospatial-to-csv`.
* While `parameters` is left empty in the example, it can optionally contain various configuration options. See below for more details.
* Other processor entries in the configuration were initially generated by the KBC UI, but note that:
  - `addCsvSuffix` parameter for the `keboola.processor-move-files` processor is set to `false`. This is because upon converting from geospatial datafiles, the CSV suffix will already have been added when output files are passed to the subsequent processors.

#### Using with other components
While the above example shows how to use this processor with one particular extractor, you can use it with most KBC components. You will likely need to tweak their configuration using the advanced JSON editor, so that this processor can be properly prepended at the beginning of the processor chain.

#### Configuration
You can always leave `parameters` for this processor empty. It resolves to a configuration with reasonable defaults:

```json
{
    "output": {
        "includeAdditionalColumns": true,
        "featureFormat": "geojson-geometry"
    },
    "input": {
        "format": {
            "kml": {
                "enabled": true,
                "glob": "**/*.kml"
            },
            "shapefile": {
                "enabled": true,
                "glob": "**/*.shp"
            },
            "geojson": {
                "enabled": true,
                "glob": "**/*.geojson"
            }
        }
    }
}
```

* `output`.`includeAdditionalColumns` specifies whether the output CSV will, in addition to the geometry column, also have columns based on other fields found in the source geospatial datafile.
* `output`.`featureFormat` specifies how exactly the geometry of features in the geospatial data will be encoded. One of:
  - `geojson-geometry` (default). GeoJSON geometry as text, e.g. `{"type":"Point","coordinates":[-77.129111523705149,38.79930767201779]}`
  - `geojson-feature`. Full GeoJSON feature, containing both its properties and geometry, as text, e.g. `{"type":"Feature","properties":{"name":"Van Dorn Street"},"geometry":{"type":"Point","coordinates":[-77.129111523705149,38.79930767201779]}}`
  - `wkt`. Well-known text representation of the geometry, e.g. `POINT (-77.129111523705149 38.79930767201779)`
* `input`.`format` allows for specific configuration of the supported formats:
  - `enabled` specified whether processing for that format is enabled. When `false`, files in this geospatial format will not be searched for (see `glob` below) and converted.
  - `glob` is the glob pattern by which files encoded in this format are searched for. By default, the pattern matches all files at any subfolder level, having the file extension common for that particular geospatial format.

For the technical looking for formal spec, the configuration is validated to conform to [parameters-schema.json](src/parameters-schema.json) JSON schema.

## License

Copyright © 2018, [Petr Krebs](https://github.com/petr-k).
Released under the [MIT License](LICENSE).

***
