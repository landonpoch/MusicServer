var myPlaylist;

$(document).ready(function(){
  loadPlaylist();
  loadEvents();
});

function loadPlaylist() {
  var cssSelectors = {}; // default
  var items = [];
  var options = {};
  $("#jquery_jplayer_1").jPlayer({swfPath: "http://debian:8080/static/jplayer/Jplayer.swf"});
  myPlaylist = new jPlayerPlaylist(cssSelectors, items, options);
}

function loadEvents() {
  $('#random').click(function (event) {
    event.preventDefault();
    loadRandomSongs();
  });
  $('#search').click(function (event) {
    event.preventDefault();
    searchSongs();
  });
  $('#clear').click(function (event) {
    event.preventDefault();
    myPlaylist.remove();
  });
  $('#libraries').click(function (event) {
    event.preventDefault();
    getLibraries();
  });
}

function loadRandomSongs() {
  $.ajax({
    url: "http://debian:8080/server/get_random_songs",
    success: function(data) {
      var songs = JSON.parse(data);
      $(songs).each(function() {
        myPlaylist.add(this);
      });
    }
  });
}

function searchSongs() {
  var searchTerm = $('#searchTerm').val();
  $.ajax({
    url: "http://debian:8080/server/search_songs?q=" + searchTerm,
    success: function(data) {
      var songs = JSON.parse(data);
      myPlaylist.remove();
      $(songs).each(function() {
        myPlaylist.add(this);
      });
    }
  });
}

function getLibraries() {
  var url = 'http://debian:8080/server/libraries'; 
  $.get(url, populateContent);
}

function populateContent(data) {
  $('#content').html(data);
}
