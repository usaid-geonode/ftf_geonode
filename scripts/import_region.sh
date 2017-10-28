#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#===============#
if [ -z "$VIRTUAL_ENV" ]; then
  VIRTUAL_ENV=/home/ubuntu/.venvs/ftf_geonode
fi
TEMP=$HOME/temp
CONFIG=$DIR/../osm.yml
LICENSE=ODbL/OSM
GEOMETRY_TYPES=( POINT )
#GEOMETRY_TYPES=( POINT POLYGON LINE )
#===============#
REGION=$1
REGION_LC=${REGION,,}
URL=$2
PBF=$3
#===============#
mkdir -p $TEMP
#===============#
for GT in "${GEOMETRY_TYPES[@]}"; do
  $VIRTUAL_ENV/bin/python $DIR/import_osm.py \
  --clean \
  --url=$URL \
  --pbf=$PBF \
  --temp=$TEMP \
  --config=$CONFIG \
  --regions=$REGION \
  --license=$LICENSE \
  --layer-name-prefix=$REGION_LC"_" \
  --layer-title-prefix="$REGION " \
  --geometry-type=$GT
done
