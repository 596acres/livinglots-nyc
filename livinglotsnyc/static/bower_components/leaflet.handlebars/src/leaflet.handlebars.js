//
// leaflet.handlebars
//
// A Leaflet plugin for handlebars-driven popups
//

(function () {
    
    function defineLeafletHandlebars(L, Handlebars) {

        L.FeatureGroup.include({

            precompileTemplate: function () {
                if (!this.handlebarsTemplate && this.options && this.options.handlebarsTemplateSelector) {
                    // Pre-compile template
                    var source = $(this.options.handlebarsTemplateSelector).html();
                    this.handlebarsTemplate = Handlebars.compile(source);
                }
                return this.handlebarsTemplate;
            },

            getTemplateContext: function (layer) {
                if (this.options.getTemplateContext) {
                    return this.options.getTemplateContext(layer);
                }
                return {
                    feature: layer.feature
                };
            },

            addLayer: function (layer) {
                // Keep most of FeatureGroup's addLayer, but try to populate each
                // layer's popup with handlebars

                if (this.hasLayer(layer)) {
                    return this;
                }

                if ('on' in layer) {
                    layer.on(L.FeatureGroup.EVENTS, this._propagateEvent, this);
                }

                L.LayerGroup.prototype.addLayer.call(this, layer);

                // If we have a handlebars template use it
                var template = this.precompileTemplate();
                if (template) {
                    try {
                        this._popupContent = this.handlebarsTemplate(this.getTemplateContext(layer));
                    }
                    catch (e) {
                        //
                    }
                }

                if (this._popupContent && layer.bindPopup) {
                    layer.bindPopup(this._popupContent, this.options.popupOptions);
                }

                return this.fire('layeradd', {layer: layer});
            }

        });
    }

    if (typeof define === 'function' && define.amd) {
        // Try to add leaflet.handlebars to Leaflet using AMD
        define(['leaflet', 'handlebars'], function (L, Handlebars) {
            defineLeafletHandlebars(L, Handlebars);
        });
    }
    else {
        // Else use the global L and Handlebars
        defineLeafletHandlebars(L, Handlebars);
    }
})();
