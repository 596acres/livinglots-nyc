var Handlebars = require('handlebars');

Handlebars.registerHelper('pick-area', function (acres, sqft) {
    if (acres > 1) {
        return acres + ' acres';
    }
    return sqft + ' sq ft';
});
