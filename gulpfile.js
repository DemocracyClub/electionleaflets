var gulp = require('gulp');
var concat = require('gulp-concat');


const packages = {
  "filepond": {
    root_location: "node_modules/filepond/",
    css: ["dist/*.css"],
    js: ["dist/*.js"]
  },
  "filepond-plugin-image-exif-orientation": {
    root_location: "node_modules/filepond-plugin-image-exif-orientation/",
    css: ["dist/*.css"],
    js: ["dist/*.js"]
  },
  "filepond-plugin-image-preview": {
    root_location: "node_modules/filepond-plugin-image-preview/",
    css: ["dist/*.css"],
    js: ["dist/*.js"]
  },
  "filerobot-image-editor": {
    root_location: "node_modules/filerobot-image-editor/",
    js: ["dist/*.js"]
  },
}


function javascript(cb) {
  var javascript_globs = []
  Object.keys(packages).forEach(function(package) {
    package_data = packages[package]
    if ('js' in package_data) {
      javascript_globs = javascript_globs.concat(package_data.js.map(el => package_data.root_location + '/' + el));
    }
  })
  return gulp.src(javascript_globs)
    .pipe(gulp.dest('electionleaflets/assets/javascript/vendor'))
}

function css(cb) {
  var css_globs = []
  Object.keys(packages).forEach(function(package) {
    package_data = packages[package]
    if ('css' in package_data) {
      css_globs = css_globs.concat(package_data.css.map(el => package_data.root_location + '/' + el));
    }
  })
  return gulp.src(css_globs)
    .pipe(gulp.dest('electionleaflets/assets/stylesheets/vendor'))
}



exports.default = gulp.series(
  javascript,
  css
);
