var _ = require('underscore');
var proj4 = require('proj4');
require('./proj4.defs');

var baseUrl = 'http://www.oasisnyc.net/map.aspx',
    vacantLotsParams = {
        etabs: 1,
        mainlayers: 'LU_VACANT,LOTS',
        zoom: 8
    };

module.exports = {
    vacantLotsUrl: function (latitude, longitude) {
        var xy = proj4('EPSG:4326', 'EPSG:2263').forward([longitude, latitude]);
        var params = _.extend({}, vacantLotsParams, { x: xy[0], y: xy[1] });
        return [baseUrl, $.param(params)].join('?');
    }
};
