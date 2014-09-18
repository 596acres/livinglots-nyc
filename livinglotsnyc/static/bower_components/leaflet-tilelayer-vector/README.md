# Leaflet GeoJSON Tile Layer

Renders GeoJSON tiles on an L.GeoJSON layer

This is a fork of [nrenner's development branch](https://github.com/nrenner/leaflet-tilelayer-vector)
of [leaflet-tilelayer-geojson](https://github.com/glenrobertson/leaflet-tilelayer-geojson).
The main addition is some logic around removing and adding layers so that 
"overzoomed" tiles are retained to avoid the flickering that happens on zoom in 
nrenner's branch, even when new data is not being loaded.

## nrenner's additions to leaflet-tilelayer-geojson:

* based on Leaflet Path vector classes instead of GeoJSON
* async queue for adding tiles to let UI render each tile immediately
* remove tiles/vectors outside viewport
* deduplication for unclipped tiles, remove common features only when no more references
* overzooming (reuse tiles for multiple zoom levels)
* loading/progress tiles
* Web Worker support

## Example usage
The following example shows a GeoJSON Tile Layer for tiles with duplicate features.

Features are deduplicated by comparing the result of the `unique` function for each feature.

        var style = {
            "clickable": true,
            "color": "#00D",
            "fillColor": "#00D",
            "weight": 1.0,
            "opacity": 0.3,
            "fillOpacity": 0.2
        };
        var hoverStyle = {
            "fillOpacity": 0.5
        };

        var geojsonURL = 'http://localhost:8000/states/{z}/{x}/{y}.json';
        var geojsonTileLayer = new L.TileLayer.GeoJSON(geojsonURL, {
                unique: function (feature) { return feature.id; }
            }, {
                style: style,
                onEachFeature: function (feature, layer) {
                    if (feature.properties) {
                        var popupString = '<div class="popup">';
                        for (var k in feature.properties) {
                            var v = feature.properties[k];
                            popupString += k + ': ' + v + '<br />';
                        }
                        popupString += '</div>';
                        layer.bindPopup(popupString);
                    }
                    if (!(layer instanceof L.Point)) {
                        layer.on('mouseover', function () {
                            layer.setStyle(hoverStyle);
                        });
                        layer.on('mouseout', function () {
                            layer.setStyle(style);
                        });
                    }
                }
            }
        );
        map.addLayer(geojsonTileLayer);


## Future development
Functionality currently being worked on:
* Re-unioning feature geometries that have been trimmed to tile boundaries

## Contributors
Thanks to the following people for helping so far:

* [Nelson Minar](https://github.com/NelsonMinar)
* [Alex Barth](https://github.com/lxbarth)
* [Pawel Paprota](https://github.com/ppawel)
