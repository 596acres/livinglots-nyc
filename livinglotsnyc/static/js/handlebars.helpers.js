var Handlebars = require('handlebars');

/*
 * A helper that formats a comparable (see django-sizecompare) into a readable
 * string.
 */
Handlebars.registerHelper('compare', function (comparable) {
    if (comparable.comparable_is === 'smaller') {
        return comparable.factor + ' times the size of ' + comparable.name;
    }
    else {
        return comparable.fraction + ' the size of ' + comparable.name;
    }
});


/*
 * A helper that picks the friendlier area to display.
 */
Handlebars.registerHelper('pick-area', function (acres, sqft) {
    if (acres > 1) {
        return acres + ' acres';
    }
    return sqft + ' sq ft';
});
