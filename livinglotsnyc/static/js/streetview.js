define(['jquery'], function ($) {

    function get_heading(lon0, lat0, lon1, lat1) {
        // Don't bother with great-circle calculations--should be close!
        var r = Math.atan2(-(lon1 - lon0), (lat1 - lat0));
        if (r < 0) {
            r += 2 * Math.PI;
        }
        var d = r * (180 / Math.PI);

        // Convert to google's heading: "True north is 0°, east is 90°,
        // south is 180°, west is 270°."
        if (d >= 45 && d < 135) { d += 180; }
        else if (d >= 225 && d < 315) { d -= 180; }
        return d;
    }

    function load_streetview(lon, lat, $elem, $errorBox) {
        var service = new google.maps.StreetViewService();

        if (!(lon && lat)) {
            return;
        }
        var latLng = new google.maps.LatLng(lat, lon);

        service.getPanoramaByLocation(latLng, 50, function (result, status) {
            // TODO result.imageDate could be useful

            if (status === google.maps.StreetViewStatus.OK) {
                var lon0 = result.location.latLng.lng(),
                    lat0 = result.location.latLng.lat();

                var pano = new google.maps.StreetViewPanorama($elem[0], {
                    pano: result.location.pano,
                    pov: {
                        heading: get_heading(lon0, lat0, lon, lat),
                        pitch: 0,
                    },
                });
            }
            else {
                $errorBox.show();
            }
        });
    }

    return {
        load_streetview: load_streetview
    };

});
