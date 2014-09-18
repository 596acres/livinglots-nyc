Leaflet.dataoptions
===================

Leaflet.dataoptions is a [Leaflet][] plugin that extends `L.Map` to read and add
configuration settings using `data-*` attributes set on the map's element. If
you specify options that are valid map options (eg, `zoom`), then those will 
override existing map options. If you specify options that are not valid map 
options, they will be added to the map options.

An attempt is made to parse option values as [JSON][]. If this fails, the 
original value is passed to the map intact.


## Usage

Include `leaflet.dataoptions.js` in your page, set the options on your map as
specified below, and create a map with a `div` as in the examples.

Leaflet.dataoptions is only tested on Leaflet version 0.6 or greater.

AMD compatible.


### Options

Define the following options when creating your map:

 - **dataOptionsPrefix**: (string) The prefix each data attribute you want 
   Leaflet.dataoptions to recognize. Optional, defaults to `data-l-`.


### Examples

Create a map that sets the `zoom` and `center` of the map and adds a `styleid`
option to the map:

```html
<div id="map"
    data-l-zoom="8"
    data-l-center="[40.71, -73.98]"
    data-l-styleid="24559"
></div>
```


## Demos

None yet.


## License

Leaflet.dataoptions is free software, and may be redistributed under the MIT
License.


 [Leaflet]: https://github.com/Leaflet/Leaflet
 [JSON]: http://json.org/
