var L = require('leaflet');

var geocode = require('./geocode').geocode;


function addCityAndState(query, city, state) {
    if (query.toLowerCase().indexOf(city) <= 0) {
        query += ', ' + city;
    }
    if (query.toLowerCase().indexOf(state) <= 0) {
        query += ', ' + state;
    }
    return query;
}

function searchByAddress($form) {
    var bounds = $form.data('bounds'),
        city = $form.data('city'),
        state = $form.data('state'),
        query = $form.find('input[type="text"]').val();

    query = addCityAndState(query, city, state);
    geocode(query, bounds, state, function (result, status) {
        // Is result valid?
        if (result === null) {
            $form.trigger('searchresulterror', $form.data('errorMessage'));
            return;
        }

        // Let the world know!
        var found_location = result.geometry.location;
        $form.trigger('searchresultfound', [{
            longitude: found_location.lng(),
            latitude: found_location.lat(),
            query_address: query,
            found_address: result.formatted_address
        }]);
    });
}

function searchLotsAndParcels($form, opts) {
    var query = $form.find('input[type="text"]').val(),
        url = $form.data('lot-search-url') + '?' + $.param({ q: query });
    $.getJSON(url, function (data) {
        if (data.results.length > 0) {
            var result = data.results[0];
            $form.trigger('searchresultfound', [{
                longitude: result.longitude,
                latitude: result.latitude
            }]);
        }
        else {
            opts.failure();
        }
    });
}

$.fn.mapsearch = function (options) {
    var $form = this;
    var warningSelector = this.data('warningSelector');

    function search(form) {
        form.trigger('searchstart');
        form.find(warningSelector).hide();
        form.find(':input[type=submit]')
            .attr('disabled', 'disabled');

        // Search by bbl, lot name, if that turns up nothing then
        // searchByAddress
        searchLotsAndParcels(form, {
            failure: function () {
                searchByAddress($form);
            }
        });
        return false;
    }

    this.keypress(function (e) {
        if (e.keyCode === '13') {
            e.preventDefault();
            return search($form);
        }
    });
    this.submit(function (e) {
        e.preventDefault();
        return search($form);
    });

    this.on('searchresulterror', function (e, message) {
        $form.find(warningSelector).text(mesage).show();

        // Done searching
        $form.find(':input[type=submit]')
            .removeAttr('disabled');
    });

    this.on('searchresultfound', function (e, message) {
        // Done searching
        $form.find(':input[type=submit]')
            .removeAttr('disabled');
    });

    return this;
};
