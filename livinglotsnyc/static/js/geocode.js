var geocoder = new google.maps.Geocoder();

function geocode(address, bounds, state, f) {
    geocoder.geocode({
        'address': address,
        'bounds': to_google_bounds(bounds),
    }, function (results, status) {
        for (var i = 0; i < results.length; i++) {
            var result_state = get_component(results[i], 'administrative_area_level_1');
            if (result_state === state) {
                return f(results[i], status);
            }
        }
        return f(null, status);
    });
}

function get_component(result, desired_type) {
    var matches = $.grep(result.address_components, function (component, i) {
        return ($.inArray(desired_type, component.types) >= 0);
    });
    if (matches.length >= 0 && matches[0] !== null) {
        return matches[0].short_name;
    }
    return null;
}

function get_street(result) {
    var street_number = get_component(result, 'street_number');
    var route = get_component(result, 'route');
    if (street_number === null || route === null) {
        return null;
    }
    return street_number + ' ' + route;
}

function get_city(result) {
    var city = get_component(result, 'sublocality');
    if (city === null) {
        city = get_component(result, 'locality');
    }
    return city;
}

function get_state(result) {
    return get_component(result, 'administrative_area_level_1');
}

function get_zip(result) {
    return get_component(result, 'postal_code');
}

function get_longitude(result) {
    return result.geometry.location.lng();
}

function get_latitude(result) {
    return result.geometry.location.lat();
}

function to_google_bounds(bounds) {
    // bounds: left, bottom, right, top
    return new google.maps.LatLngBounds(
        new google.maps.LatLng(bounds[1], bounds[0]),
        new google.maps.LatLng(bounds[3], bounds[2])
    );
}

module.exports = {
    geocode: geocode
};
