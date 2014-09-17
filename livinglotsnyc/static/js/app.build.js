({

    baseUrl: '.',

    mainConfigFile: 'app.js',

    name: '../bower_components/almond/almond',
    out: '../main-built.js',
    include: [

        // Main module
        'main',

        // Per-page modules go here

        // require()d dependencies
        'fancybox',
        'mappage',
        'underscore'
    ],
    insertRequire: ['main'],

    optimizeCss: "none",
    optimize: "uglify2",

    preserveLicenseComments: true,
    
})
