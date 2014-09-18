//
// leaflet.dataoptions
//
// A Leaflet plugin that makes it easy to configure a Leaflet map using data
// attributes on the map's DOM element.
//

(function () {
    
    function defineDataOptions(L) {

        L.Map = L.Map.extend({

            // Override the default constructor to get options from data 
            // attributes
            initialize: function (id, options) {
                // Get the data prefix for attribute names
                var prefix = 'data-l-';
                if (options !== undefined && options.dataOptionsPrefix !== undefined) {
                    prefix = options.dataOptionsPrefix;
                }

                // Find options given by data attribute, add to existing options
                var dataAttributeOptions = this.loadDataAttributeOptions(id, prefix);
                options = L.extend(dataAttributeOptions, options);

                // Carry on as usual
                L.Map.__super__.initialize.call(this, id, options);
            },

            loadDataAttributeOptions: function (id, prefix) {
                var element = L.DomUtil.get(id),
                    attributes = element.attributes,
                    length = attributes.length,
                    newOptions = {};
                for (var i = 0; i < length; i++) {
                    var attribute = attributes[i];
                    if (attribute.name.search(prefix) === 0) {
                        var name = attribute.name.slice(prefix.length),
                            camelCaseName = this.camelCaseDataAttributeName(name),
                            value = this.parseDataAttributeValue(attribute.value);
                        newOptions[camelCaseName] = newOptions[name] = value;
                    }
                }
                return newOptions;
            },

            camelCaseDataAttributeName: function (name) {
                var nameParts = name.split('-'),
                    camelCaseName = nameParts[0];
                for (var i = 1; i < nameParts.length; i++) {
                    camelCaseName += nameParts[i][0].toUpperCase();
                    camelCaseName += nameParts[i].slice(1);
                }
                return camelCaseName;
            },

            parseDataAttributeValue: function (value) {
                try {
                    return JSON.parse(value);
                }
                catch (e) {
                    // If parsing as JSON fails, return original string
                    return value;
                }
            }

        });

    }

    if (typeof define === 'function' && define.amd) {
        // Try to add dataoptions to Leaflet using AMD
        define(['leaflet'], function (L) {
            defineDataOptions(L);
        });
    }
    else {
        // Else use the global L
        defineDataOptions(L);
    }

})();
