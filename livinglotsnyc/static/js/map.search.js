define(
    [
        'jquery',
        'geocode',
    ], function ($, geocode) {

        function addCityAndState(query, city, state) {
            if (query.toLowerCase().indexOf(city) <= 0) {
                query += ', ' + city;
            }
            if (query.toLowerCase().indexOf(state) <= 0) {
                query += ', ' + state;
            }
            return query;
        }

        function searchByAddress(form) {
            form = $(form);
            form.trigger('searchstart');
            var warningSelector = form.data('warningSelector'),
                bounds = form.data('bounds'),
                city = form.data('city'),
                state = form.data('state'),
                query = form.find('input[type="text"]').val();

            form.find(warningSelector).hide();
            form.find(':input[type=submit]')
                .attr('disabled', 'disabled');

            query = addCityAndState(query, city, state);

            geocode(query, bounds, state, function (result, status) {
                // Done searching
                form.find(':input[type=submit]')
                    .removeAttr('disabled');

                // Is result valid?
                if (result === null) {
                    form.find(warningSelector)
                        .text(form.data('errorMessage'))
                        .show();
                    return;
                }

                // Let the world know!
                var found_location = result.geometry.location;
                form.trigger('searchresultfound', [{
                    longitude: found_location.lng(),
                    latitude: found_location.lat(),
                    query_address: query,
                    found_address: result.formatted_address,
                }]);
            });
        }

        $.fn.mapsearch = function (options) {

            this.keypress(function (e) {
                if (e.keyCode === '13') {
                    e.preventDefault();
                    searchByAddress(this);
                    return false;
                }
            });
            this.submit(function (e) {
                e.preventDefault();
                searchByAddress(this);
                return false;
            });

            return this;
        };
    }
);
