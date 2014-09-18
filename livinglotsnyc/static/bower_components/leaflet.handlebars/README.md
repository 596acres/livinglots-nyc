Leaflet.handlebars
===================

Leaflet.handlebars is a [Leaflet][] plugin that extends `L.FeatureGroup` to use
[Handlebars][] templates in each feature's popup.


## Usage

Include `leaflet.handlebars.js` in your page, set the options on your
`FeatureGroup` as specified below.

Leaflet.handlebars is only tested on Leaflet version 0.6 or greater.

Requires Handlebars (obviously). AMD compatible.


### Options

Define the following options on your `FeatureGroup` (eg, an `L.GeoJSON`):

 - **getTemplateContext**: (function) A function that takes the layer that a 
   popup is being created for and returns an object that will serve as the 
   context for the template. Optional. If not provided, the context will be
   consist of the layer's feature, which will be called `feature`.
 - **handlebarsTemplateSelector**: (string) The selector for the Handlebars
   template. Required.


### Examples

Create a GeoJSON layer, each feature having a popup as defined in a Handlebars
template with `id` `popup-template`:

```javascript
var geojsonlayer = L.geoJson(data, {
    handlebarsTemplateSelector: '#popup-template'
});
```

Slightly more complicated, create a GeoJSON layer and customize the context
given to the template for each layer:

```javascript
var geojsonlayer = L.geoJson(data, {
    handlebarsTemplateSelector: '#popup-template',
    getTemplateContext: function (layer) {
        return {
            detailUrl: '/things/' + layer.feature.id,
            feature: layer.feature
        };
    }
});
```


## Demos

None yet.


## License

Leaflet.handlebars is free software, and may be redistributed under the MIT
License.


 [Leaflet]: https://github.com/Leaflet/Leaflet
 [Handlebars]: http://handlebarsjs.com/
