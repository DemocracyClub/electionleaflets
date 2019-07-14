/* jshint unused: false */
(function(){
  'use strict';

  var paths = {
    tmp: 'gulptmp/',
    dest: 'electionleaflets/media/',
    src: 'electionleaflets/assets-src/',
    fonts: [],
    images: ['electionleaflets/assets-src/images'],
    scripts: {},
    styles: [],
    standalone: [],
  };

  paths.styles.push(paths.src + 'stylesheets/**/*.scss');
  paths.styles.push(paths.src + 'stylesheets/**/*.css');
  paths.styles.push(paths.src + 'vendor/**/*.scss');
  paths.styles.push(paths.src + 'vendor/**/*.css');

  paths.standalone.push(paths.src + 'vendor/Jcrop/css/jquery.Jcrop.min.css');
  paths.standalone.push(paths.src + 'vendor/foundation/css/foundation.css');
  paths.standalone.push(paths.src + 'vendor/foundation/css/foundation.css.map');

  // images
  paths.images.push(paths.src + 'images/**/*');

  paths.fonts.push(paths.src + 'fonts/*.{otf,eot,svg,ttf,woff,woff2}');
  paths.fonts.push(paths.tmp + 'fonts/*.{otf,eot,svg,ttf,woff,woff2}');
  paths.fonts.push(paths.src + 'vendor/**/*.{otf,eot,svg,ttf,woff,woff2}');
  paths.fonts.push(paths.tmp + 'vendor/**/*.{otf,eot,svg,ttf,woff,woff2}');

  // scripts
  paths.scripts = {
    vendor: [
      paths.src + 'vendor/jquery/dist/jquery.js',
      paths.src + 'vendor/masonry/index.js',
      paths.src + 'vendor/leaflet/index.js',
      paths.src + 'vendor/jquery.tablesorter.min.js',
      paths.src + 'vendor/jquery.zoom.min.js'

    ],
    app: [
        paths.src + 'javascript/app.js',
    ],
    standalone: [
        paths.src + 'javascript/admin.js',
        paths.src + 'vendor/Jcrop/js/jquery.Jcrop.min.js',
        paths.src + 'vendor/foundation/js/foundation.js',
        paths.src + 'vendor/modernizr/modernizr.js',
        paths.src + 'vendor/jquery/dist/jquery.js',
        paths.src + 'vendor/jquery.tablesorter.min.js'
    ]
  };


  var gulp = require('gulp'),
    concat = require('gulp-concat'),
    cleanCss = require('gulp-clean-css'),
    rename = require('gulp-rename'),
    ignore = require('gulp-ignore'),
    watch = require('gulp-watch'),
    imagemin = require('gulp-imagemin'),
    sass = require('gulp-sass');

  gulp.task('clean-pre', function() {
    return gulp
      .src([paths.dest, paths.tmp], {read: false})
      .pipe(ignore('node_modules/**'))
  });

  gulp.task('copy-fonts', function() {
    gulp.src(paths.fonts)
      .pipe(gulp.dest(paths.dest + 'fonts/'));
  });

  // optimise images
  gulp.task('images', function() {
    gulp
      .src(paths.images)
      .pipe(imagemin({optimizationLevel: 5}))
      .pipe(gulp.dest(paths.dest + 'images'));
  });


  // copy & compile scss
  gulp.task('copy-sass', function() {
    return gulp
      .src(paths.styles)
      .pipe(gulp.dest(paths.tmp + 'stylesheets/'));
  });


  gulp.task('sass', function() {
    return sass(paths.tmp + 'stylesheets/main.scss', {
        lineNumbers: true,
        style: 'compact'
      })
      .on('error', function (err) { console.log('ERROR: '+err.message); })
      .pipe(gulp.dest(paths.tmp + 'stylesheets/'));
  });



  gulp.task('css', ['copy-sass', 'sass'], function() {
    gulp
      .src(paths.tmp + 'stylesheets/main.css')
      .pipe(cleanCss())
      .pipe(rename({ suffix: '.min' }))
      .pipe(gulp.dest(paths.dest + 'stylesheets/'));
  });


  gulp.task('standalone_css', function() {
    gulp
      .src(paths.standalone)
      .pipe(gulp.dest(paths.dest + 'stylesheets/'));
  });

  gulp.task('scripts', function() {
    var all_scripts = paths.scripts.vendor.concat(paths.scripts.app);

    return gulp.src(all_scripts)
      // .pipe(uglify({ mangle: true }))
      .pipe(concat('electionleaflets.main.min.js'))
      .pipe(gulp.dest(paths.dest + 'javascript/'));
  });

  gulp.task('standalone_scripts', function() {
    return gulp.src(paths.scripts.standalone)
      // .pipe(uglify({ mangle: true }))
      // .pipe(concat('electionleaflets.main.min.js'))
      .pipe(gulp.dest(paths.dest + 'javascript/'));
  });

  gulp.task('watch', function() {
    //watches SCSS files for changes
    gulp.watch(paths.src + '**/*.scss', ['css']);

    //watches JavaScript files for changes
    gulp.watch(paths.src + '**/*.js', ['templates', 'scripts', 'standalone_scripts']);
    gulp.watch(paths.tmp + '**/*.js', ['scripts']);
  });

  gulp.task('build', ['clean-pre', 'css', 'scripts']);
  gulp.task('default', [
    'images',
    'copy-fonts',
    'css',
    'scripts',
    'standalone_scripts',
    'standalone_css',
    'watch'
  ]);

})();
