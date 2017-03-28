#!/bin/bash
/home/vagrant/.venvs/geonode/bin/python /home/vagrant/ftf_geonode.git/scripts/import_osm.py \
--url=http://download.geofabrik.de/asia/nepal-latest.osm.pbf \
--pbf=/home/vagrant/nepal-latest.osm.pbf \
--temp=/home/vagrant/ftf_geonode.git/temp \
--config=osm.yml \
--regions=Nepal \
--license=ODbL/OSM \
--geometry-type=POINT \
--layer-name-prefix=nepal_ \
--layer-title-prefix="Nepal "
