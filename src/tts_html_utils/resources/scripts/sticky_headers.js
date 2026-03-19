var table = document.querySelectorAll('table.sticky-header');
for (var i = 0; i < table.length; i++) {
  headers = table[i].getElementsByTagName('thead');
  if (headers) {
    var hoff = 0;
    for (var j = 0; j < headers.length; j++) {
      headers[j].style.top = hoff + 'px';
      hoff += headers[j].offsetHeight;
    }
  }
}