/*
 After you have changed the settings at "Your code goes here",
 run this with one of these options:
  "grunt" alone creates a new, completed images directory
  "grunt clean" removes the images directory
  "grunt responsive_images" re-processes images without removing the old ones
*/

module.exports = function(grunt) {

    grunt.initConfig({
      image_resize: {
        options: {
          width: 320,
          height: 212,
          overwrite: true
        },
        resize: {
          files: [{
            expand: true,
            src: ['*.{gif,jpg,png}'],
            cwd: 'static/images_src/',
            dest: 'tmp'
          }]
        }
      },

      responsive_images: {
        dev: {
          options: {},
          sizes: [{
            name: 'small',
            width: 320,
            height: 212,
            suffix: "_small"
          },{
            name: 'medium',
            width: 640,
            suffix: "_medium"
          },{
            name: "large",
            width: 1024,
            suffix: "_x2",
            quality: 0.6
          }],
          files: [{
            expand: true,
            src: ['*.{gif,jpg,png}'],
            cwd: 'tmp',
            dest: 'static/images/'
          }]
        }
    },
  

    /* Clear out the images directory if it exists */
    clean: {
      dev: {
        src: ['images'],
      },
    },

    /* Copy the "fixed" images that don't go through processing into the images/directory */
    copy: {
      dev: {
        files: [{
          expand: true,
          src: 'static/images_src/*.{gif,jpg,png}',
          dest: 'static/images/'
        }]
      },
    },
  });
  
  
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-image-resize');
  grunt.loadNpmTasks('grunt-responsive-images');
  grunt.registerTask('default', ['clean', 'copy', 'image_resize','responsive_images']);
  

};
