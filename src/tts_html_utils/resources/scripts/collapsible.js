var elem, i

function update_sibling(elem, sib) {
  if (elem.classList.contains('active-clicked')) {
    sib.classList.add('collapsed');
  } else {
    sib.classList.remove('collapsed');
  }
}

function update_one_sibling(elem) {
  var sib = elem.nextElementSibling;
  update_sibling(elem, sib)
}

function update_all_siblings(elem) {
  var sib = elem.nextElementSibling;
  while (sib) {
    update_sibling(elem, sib);
    sib = sib.nextElementSibling;
  }
}

elem = document.getElementsByClassName("collapsible");
for (i = 0; i < elem.length; i++) {
  update_one_sibling(elem[i]);
  elem[i].addEventListener("click", function() {
    this.classList.toggle('active-clicked')
    update_one_sibling(this);
  });
}

elem = document.getElementsByClassName("collapsible-group");
for (i = 0; i < elem.length; i++) {
  update_all_siblings(elem[i]);
  elem[i].addEventListener("click", function() {
    this.classList.toggle('active-clicked')
    update_all_siblings(this);
  });
}