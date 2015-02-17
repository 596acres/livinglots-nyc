module.exports = function(grunt) {
    grunt.initConfig({
        browserify: {
            dev: {
                options: {
                    browserifyOptions: {
                        debug: true
                    },
                    watch: true
                },
                src: 'js/main.js',
                dest: 'js/bundle.dev.js'
            },
            production: {
                options: {
                    watch: true
                },
                src: '<%= browserify.dev.src %>',
                dest: 'js/bundle.js'
            }
        },

        cssmin: {
            minify: {
                src: '<%= less.production.dest %>',
                dest: 'css/style.min.css'
            }
        },

        jshint: {
            all: {
                files: {
                    src: [
                        "js/*.js",
                        '!<%= browserify.dev.dest %>',
                        '!<%= browserify.production.dest %>',
                        '!<%= uglify.production.dest %>'
                    ]
                }
            }
        },

        less: {
            dev: {
                options: {
                    paths: ["css"],
                    sourceMap: true
                },
                src: "css/style.less",
                dest: "css/style.dev.css"
            },
            production: {
                options: {
                    paths: ['css'],
                    yuicompress: true
                },
                src: '<%= less.dev.src %>',
                dest: 'css/style.css'
            }
        },

        uglify: {
            production: {
                src: '<%= browserify.production.dest %>',
                dest: 'js/bundle.min.js'
            }
        },

        watch: {
            jshint: {
                files: ["js/*.js", "!bundle.js"],
                tasks: ["jshint"]
            },

            less: {
                files: ["css/*.less", "css/*/*.less"],
                tasks: ["less", "cssmin"]
            },

            uglify: {
                files: ['<%= browserify.production.dest %>'],
                tasks: ['uglify']
            }
        }
    });

    grunt.loadNpmTasks('grunt-browserify');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask("dev", ["browserify", "watch"]);
};
