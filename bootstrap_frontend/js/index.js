var inp = $('#movie_search');
var movie_maps = [];
var currentFocus;
inp.on("keydown", function(e) {
  var x = $('#'+this.id+'_autocomplete-list')[0];
  if (x) x = x.getElementsByTagName("div");
  if (e.keyCode == 40) {
    currentFocus++;
    addActive(x);
  } else if (e.keyCode == 38) {
    currentFocus--;
    addActive(x);
  } else if (e.keyCode == 13) {
    e.preventDefault();
    if (currentFocus > -1) {
      if (x) x[currentFocus].click();
    }
  }
});
inp.on("input", function(e) {
  var a, b, i, val = this.value;
  closeAllLists();
  if (!val) { return false;}
  currentFocus = -1;
  a = $('<div></div>');
  a = a.attr('id',this.id + '_autocomplete-list');
  a = a.attr('class','autocomplete-items');
  a = a[0];
  $(this).parent().append(a);

  var prefix = this.value;
  var limit = 5;
  var offset = 0;
  var url = 'http://0.0.0.0:5000/autocomplete/'+prefix+'_'+limit+'_'+offset;
  $.get(url, function(data){
    for (i = 0; i < data.length; i++) {
      movie_maps[i] = {}
      movie_maps[i].key = data[i]['name']
      movie_maps[i].value = data[i]['_id']
      if (data[i]['name'].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
        b = $('<div></div>');
        b[0].innerHTML = "<strong>" + data[i]['name'].substr(0, val.length) + "</strong>";
        b[0].innerHTML += data[i]['name'].substr(val.length);
        b[0].innerHTML += "<input type='hidden' value='" + data[i]['name'] + "'>";
        b.on("click", function(e) {
          inp.val(this.getElementsByTagName("input")[0].value);
          var id = getMovieID(this.getElementsByTagName("input")[0].value);
          getMovieInformation(id);
          closeAllLists();
        });
        $(a).append(b);
      }
    }
  },'json');

});
function addActive(x) {
  if (!x) return false;
  removeActive(x);
  if (currentFocus >= x.length) currentFocus = 0;
  if (currentFocus < 0) currentFocus = (x.length - 1);
  x[currentFocus].classList.add("autocomplete-active");
}
function removeActive(x) {
  for (var i = 0; i < x.length; i++) {
    x[i].classList.remove("autocomplete-active");
  }
}
function closeAllLists(elmnt) {
  var x = $('.autocomplete-items');
  for (var i = 0; i < x.length; i++) {
    if (elmnt != x[i] && elmnt != inp) {
      x[i].parentNode.removeChild(x[i]);
    }
  }
}
document.addEventListener("click", function (e) {
  closeAllLists(e.target);
});
function getMovieID(movie_name) {
  for (var i = 0; i < movie_maps.length; i++) {
    if (movie_maps[i]['key'] == movie_name) {
      return movie_maps[i]['value'];
    }
  }
}
function getMovieInformation(movie_id) {
  var url = 'http://0.0.0.0:5000/movies/'+movie_id;
  $.get(url, function(data){
    $('#movie_title').html(data[0]['name']);
    $('#release_year').html(data[0]['release_year']);
    $('#rating').html(data[0]['rating']);
    $('#storyline').html(data[0]['briefs']);
  },'json');
}
