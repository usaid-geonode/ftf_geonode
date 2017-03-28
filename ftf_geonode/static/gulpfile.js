var gulp = require('gulp');
var gutil = require('gulp-util');
var pkg = require('./package.json');
var concat = require('gulp-concat');
var less = require('gulp-less');
var del = require('del');

var cwd = __dirname;
var ts = (new Date).getTime();

if (!String.prototype.startsWith) {
  String.prototype.startsWith = function(searchString, position) {
    position = position || 0;
    return this.indexOf(searchString, position) === position;
  };
}

if (!String.prototype.endsWith) {
  String.prototype.endsWith = function(searchString, position) {
      var subjectString = this.toString();
      if (typeof position !== 'number' || !isFinite(position) || Math.floor(position) !== position || position > subjectString.length) {
        position = subjectString.length;
      }
      position -= searchString.length;
      var lastIndex = subjectString.indexOf(searchString, position);
      return lastIndex !== -1 && lastIndex === position;
  };
}

gulp.task('clean:css', [], function () {
  return del([ './css/**/*' ]);
});

gulp.task('compile:site_base.css', [], function() {
  return gulp.src(["./less/site_base.less"], {base: './'})
    .pipe(less({}))
    .pipe(concat("site_base.css"))
    .pipe(gulp.dest("./css"));
});

gulp.task('watch', function() {
  gulp.watch("./less/**/*", ['clean:css', 'compile:site_base.css']);
});

gulp.task('default', ['watch', 'clean:css', 'compile:site_base.css']);
