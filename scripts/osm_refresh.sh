#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#===============#
if [ -z "$(command -v osmconvert)" ]; then
  echo "osmconvert does not exist.  Please install osmctools with \"sudo apt-get install osmctools\"."
  exit 1
fi
if [ -z "$(command -v ogr2ogr)" ]; then
  echo "ogr2ogr does not exist.  Please install ogr2ogr with \"sudo apt-get install gdal-bin\"."
  exit 1
fi
#===============#
echo "Starting OSM import ..."
if [ -z "$OSM_CONFIG_FILE" ]; then
  wget "https://raw.githubusercontent.com/ftf-geonode/osm_extract_config.tsv/master/osm_extract_config.tsv" -O $HOME/osm_extract_config.tsv
  OSM_CONFIG_FILE=$HOME/osm_extract_config.tsv
fi
mapfile -t OSM_CONFIG < $OSM_CONFIG_FILE
for i in "${!OSM_CONFIG[@]}"; do
  if (( i > 0 )); then
    LINE=${OSM_CONFIG[$i]}
    REGION_NAME=$(cut -f 1 -d ' ' <<< $LINE)
    REGION_URL=$(cut -f 2 -d ' ' <<< $LINE)
    REGION_FILENAME=${REGION_URL##*/}
    echo "Importing $REGION_NAME from $REGION_URL"
    bash $DIR/import_region.sh $REGION_NAME $REGION_URL $HOME/$REGION_FILENAME
  fi
done

#bash $DIR/import_region.sh Mauritius http://download.geofabrik.de/africa/mauritius-latest.osm.pbf $HOME/mauritius-latest.osm.pbf
#bash import_region.sh Uganda http://download.geofabrik.de/africa/uganda-latest.osm.pbf $HOME/uganda-latest.osm.pbf
#bash import_region.sh Nepal http://download.geofabrik.de/asia/nepal-latest.osm.pbf $HOME/nepal-latest.osm.pbf
echo "Done"
