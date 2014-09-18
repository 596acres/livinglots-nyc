module.exports = function(grunt) {
    grunt.initConfig({
        browserify: {
            standalone: {
                options: {
                    watch: true
                },
                src: ['js/main.js'],
                dest: 'js/bundle.js'
            }
        },

        cssmin: {
            minify: {
                src: 'css/style.css',
                dest: 'css/style.min.css'
            }
        },

        jshint: {
            all: {
                files: {
                    src: ["js/*.js", "!js/bundle.js"]
                }
            }
        },

        less: {
            development: {
                options: {
                    paths: ["css"],
                    yuicompress: true
                },
                files: {
                    "css/style.css": "css/style.less"
                }
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
            }
        }
    });

    grunt.loadNpmTasks('grunt-browserify');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask("dev", ["browserify", "watch"]);
};
