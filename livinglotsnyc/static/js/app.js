requirejs.config({
    baseUrl: "/static/js",
    paths: {
        "bootstrap": "../bower_components/bootstrap/dist/js/bootstrap",
        "django": "djangojs/django",
        "fancybox": "../bower_components/fancybox/source/jquery.fancybox",
        "jquery": "../bower_components/jquery/jquery",
        "jquery.infinitescroll": "../bower_components/infinite-scroll/jquery.infinitescroll",
        "handlebars": "../bower_components/handlebars/handlebars",
        "leaflet": "../bower_components/leaflet/leaflet-src",
        "leaflet.bing": "../bower_components/leaflet-plugins/layer/tile/Bing",
        "leaflet.dataoptions": "../bower_components/leaflet.dataoptions/src/leaflet.dataoptions",
        "leaflet.handlebars": "../bower_components/leaflet.handlebars/src/leaflet.handlebars",
        "leaflet.hash": "../bower_components/leaflet-hash/leaflet-hash",
        "leaflet.loading": "../bower_components/leaflet.loading/src/Control.Loading",
        "leaflet.usermarker": "../bower_components/leaflet.usermarker/src/leaflet.usermarker",
        "requirejs": "../bower_components/requirejs",
        "select2": "../bower_components/select2/select2",
        "spin": "../bower_components/spin.js/spin",
        "text": "../bower_components/requirejs-text/text",
        "underscore": "../bower_components/underscore/underscore",

        // TileLayer.GeoJSON paths
        "communist": "../bower_components/leaflet-tilelayer-vector/lib/communist.min",
        "TileCache": "../bower_components/leaflet-tilelayer-vector/src/TileCache",
        "AbstractWorker": "../bower_components/leaflet-tilelayer-vector/src/AbstractWorker",
        "CommunistWorker": "../bower_components/leaflet-tilelayer-vector/src/CommunistWorker",
        "TileLayer.GeoJSON": "../bower_components/leaflet-tilelayer-vector/src/TileLayer.GeoJSON",
        "TileLayer.Overzoom": "../bower_components/leaflet-tilelayer-vector/src/TileLayer.Overzoom",
        "TileQueue": "../bower_components/leaflet-tilelayer-vector/src/TileQueue"
    },
    shim: {
        "bootstrap": ["jquery"],
        "django": {
            "deps": ["jquery"],
            "exports": "Django"
        },
        "handlebars": {
            "exports": "Handlebars"
        },
        "jquery.infinitescroll": ["jquery"],
        "leaflet.bing": ["leaflet"],
        "leaflet.hash": ["leaflet"],
        "leaflet.usermarker": ["leaflet"],
        "underscore": {
            "exports": "_"
        }
    }
});

// Load the main app module to start the app
requirejs(["main"]);
