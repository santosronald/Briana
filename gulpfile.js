/**
 * Created by manu on 29/06/15.
 */
var gulp = require('gulp');
var sass = require('gulp-ruby-sass');
var notify = require('gulp-notify');
var bower = require('gulp-bower');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');
var concat = require('gulp-concat');

var config = {
  sassPath: './static/sass',
  jsPath: './static/js',
  bowerDir: './bower_components'
};

var scripts_path = [
  config.bowerDir + '/jquery/dist/jquery.js',
  config.bowerDir + '/bootstrap-sass-official/assets/javascripts/bootstrap.js',
  config.bowerDir + '/material-design-lite/material.js',
  config.bowerDir + '/slick-carousel/slick/slick.js',
  config.jsPath + '/main.js'
];

gulp.task('bower', function() { 
  return bower().pipe(gulp.dest(config.bowerDir))
});

gulp.task('icons', function() { 
  return gulp.src(config.bowerDir + '/fontawesome/fonts/**.*').pipe(gulp.dest('./static/fonts')); 
});

gulp.task('scripts', function() {
  if (process.env.NODE_ENV == "development") {
    return gulp.src(scripts_path)
      .pipe(sourcemaps.init())
      .pipe(concat('all.min.js'))
      .pipe(uglify({
        mangle: false
      }))
      .pipe(sourcemaps.write())
      .pipe(gulp.dest('static/js/build'));
  } else {
    return gulp.src(scripts_path)
      .pipe(concat('all.min.js'))
      .pipe(uglify({
        mangle: false
      }))
      .pipe(gulp.dest('static/js/build'));
  }
});

gulp.task('css', function() { 
  return sass(config.sassPath + '/style.scss', {
      style: 'compressed',
      loadPath: [
        config.bowerDir + '/bootstrap-sass-official/assets/stylesheets',
        config.bowerDir + '/fontawesome/scss',
        config.bowerDir + '/sass-mediaqueries',
        config.bowerDir + '/material-design-lite/src',
        config.bowerDir + '/slick-carousel/slick/slick-theme.scss',
        config.bowerDir + '/slick-carousel/slick/slick.scss'

      ]

    })
    .on("error", notify.onError(function(error) {
      return "Error: " + error.message;
    }))
    .pipe(gulp.dest('./static/css'));
});

gulp.task('watch', function() {
  gulp.watch(config.sassPath + '*.scss', ['css']); 
});

gulp.task('default', ['bower', 'icons', 'css', 'scripts']);
