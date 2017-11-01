#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
START_TIME=$SECONDS
#===============#
printUsage ()
{
  echo "Usage: osm_refresh.sh OSM_CONFIG_PATH [OSM_CONFIG_URL UPDATE]"
  echo "  * OSM_CONFIG_PATH is a path to a tab delimited values file with 2 columns: Region & URL.  Region is a name of a region to be used in GeoNode and url is a link to an .osm.pbf file."
  echo "  * OSM_CONFIG_URL is a url that points to the osm config file.  If the file does not exist or update does not equal to 1, then the file will be downloaded and save to the OSM_CONFIG_PATH."
  echo "  * UPDATE if update is equal to \"1\" then the file at OSM_CONFIG_PATH is replaced with the new file from OSM_CONFIG_URL."
  echo "  * Example: osm_refresh.sh osm_extract_config.tsv https://raw.githubusercontent.com/usaid-geonode/usaid_geonode_config/master/osm_extract_config.tsv"
  echo "  * Example: osm_refresh.sh /home/ubuntu/osm_extract_config.tsv https://raw.githubusercontent.com/usaid-geonode/usaid_geonode_config/master/osm_extract_config.tsv 1"
}
#===============#
if [ "$#" -lt 1 ]; then
    echo "Error: Illegal number of arguments"
    printUsage
    exit 1
fi
if [ "$#" -gt 3 ]; then
    echo "Error: Illegal number of arguments"
    printUsage
    exit 1
fi
#===============#
OSM_CONFIG_PATH=$1
OSM_CONFIG_URL=$2
OSM_CONFIG_UPDATE=$3
OSM_CONFIG_EXISTS=$(readlink -e $OSM_CONFIG_PATH)
#===============#
echo "Starting OSM import ..."
if [ -z "$OSM_CONFIG_EXISTS" ] || [ "$OSM_CONFIG_UPDATE" == "1" ]; then
  if [ -z "$OSM_CONFIG_URL" ]; then
    echo "Error: Missing OSM_CONFIG_URL"
    printUsage
    exit 1
  fi
  if [ "$OSM_CONFIG_UPDATE" == "1" ]; then
    echo "Removing existing OSM config file."
    rm  $OSM_CONFIG_PATH
  fi
  echo "Downloading new OSM config file from < $OSM_CONFIG_URL >"
  wget "$OSM_CONFIG_URL" -O $OSM_CONFIG_PATH
  echo "New OSM config file save to < $OSM_CONFIG_PATH >"
fi
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
exit 1
mapfile -t OSM_CONFIG < $OSM_CONFIG_PATH
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
#===============#
ELAPSED_TIME=$(($SECONDS - $START_TIME))
echo "Done in $ELAPSED_TIME seconds"
