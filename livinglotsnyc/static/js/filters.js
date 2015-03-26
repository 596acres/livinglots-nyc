var _ = require('underscore');
var turf = {};
turf.inside = require('turf-inside');
turf.point = require('turf-point');


var defaultFilters = {
    layers: ['organizing', 'in_use', 'no_people', 'in_use_started_here'],
    ownerTypes: ['private_opt_in', 'public'],
    parents_only: true
};


var renamedFilters = {
    ownerTypes: 'owner_types',
    privateOwnerPks: 'private_owners',
    publicOwnerPks: 'public_owners'
};


function normalizeFilters(filters) {
    // Normalize filters that are arrays
    _.each(['layers', 'ownerTypes', 'privateOwnerPks', 'publicOwnerPks'], function (key) {
        if (filters[key]) {
            filters[key] = filters[key].join(',');
        }
    });

    // Rename filters for url
    _.each(renamedFilters, function (newName, oldName) {
        if (filters[oldName] !== undefined) {
            filters[newName] = filters[oldName];
            delete filters[oldName];
        }
    });

    // Handle boundary
    if (filters.boundaryLayer && filters.boundaryPk) {
        filters.boundary = filters.boundaryLayer + '::' + filters.boundaryPk;
        delete filters.boundaryPk;
        delete filters.boundaryLayer;
    }
    return filters;
}


function toParams(filters) {
    return normalizeFilters(_.extend({}, defaultFilters, filters));
}


module.exports = {
    lotShouldAppear: function (lot, filters, boundariesLayer) {
        // Should a lot show up on the map?
        //
        // The filters UI is split into three categories:
        //  * boundaries
        //  * ownership
        //  * layers / categories
        //
        // We follow these three categories to find a reason to exclude a lot.
        // If a lot fails for any of the three categories, it fails for all and
        // is not shown.
        var ownershipLayers = ['public', 'private_opt_in'],
            peopleInvolvedLayers = ['in_use', 'in_use_started_here', 'organizing'],
            lotLayers = lot.feature.properties.layers.split(','),
            lotLayersOwnership = _.intersection(lotLayers, ownershipLayers),
            lotLayersNotOwnership = _.difference(lotLayers, ownershipLayers);

        /*
         * Boundaries
         */

        // Look at current boundary, hide anything not in it
        if (boundariesLayer.getLayers().length > 0) {
            var centroid = lot.getBounds().getCenter(),
                point = turf.point([centroid.lng, centroid.lat]),
                polygon = boundariesLayer.getLayers()[0].toGeoJSON();
            if (!turf.inside(point, polygon)) {
                return false;
            }
        }

        /*
         * Ownership
         */

        // Ownership types
        if (_.isEmpty(_.intersection(lotLayersOwnership, filters.owner_types))) {
            return false;
        }

        // Individual owners
        if (filters.public_owners && _.contains(lotLayersOwnership, 'public') &&
                !_.contains(filters.public_owners, lot.feature.properties.owner)) {
            return false;
        }
        if (filters.private_owners && _.contains(lotLayersOwnership, 'private_opt_in') &&
                !_.contains(filters.private_owners, lot.feature.properties.owner)) {
            return false;
        }

        /*
         * Layers
         */

        // No people involved (just vacant): no_people selected, lot has no
        // people-involving layers associated with it. This is considered
        // separate to gutterspace, so we check for gutterspace, too.
        if (_.contains(filters.layers, 'no_people') &&
            _.isEmpty(_.intersection(peopleInvolvedLayers, lotLayersNotOwnership)) &&
            !_.contains(lotLayers, 'gutterspace')) {
            return true;
        }

        // Other layers
        if (_.isEmpty(_.intersection(lotLayersNotOwnership, filters.layers))) {
            return false;
        }

        return true;
    },

    paramsToFilters: function (params) {
        var filters = _.extend({}, params);
        filters.layers = filters.layers.split(',');
        filters.owner_types = filters.owner_types.split(',');
        if (filters.public_owners) {
            filters.public_owners = _.map(filters.public_owners.split(','), function (ownerPk) {
                return parseInt(ownerPk);
            });
        }
        if (filters.private_owners) {
            filters.private_owners = _.map(filters.private_owners.split(','), function (ownerPk) {
                return parseInt(ownerPk);
            });
        }
        return filters;
    },

    // Take the current state of the map and filters to create params suitable
    // for requests (eg counts)
    filtersToParams: function (map, options) {
        var filters = {
            publicOwnerPks: [$('.filter-owner-public').val()],
            privateOwnerPks: [$('.filter-owner-private').val()]
        };
        filters.layers = _.map($('.filter-layer:checked'), function (layer) {
            return $(layer).attr('name'); 
        });
        filters.ownerTypes = _.map($('.filter-owner-type:checked'), function (ownerType) {
            return $(ownerType).attr('name'); 
        });

        // Add boundary, if any
        $.each($('.filter-boundaries'), function () {
            if ($(this).val() !== '') {
                filters.boundaryLayer = $(this).data('layer');
                filters.boundaryPk = $(this).val();
            }
        });

        var params = toParams(filters);

        // Add BBOX if requested
        if (options && options.bbox) {
            params.bbox = map.getBounds().toBBoxString();
        }

        return params;
    },

    toParams: toParams
};
