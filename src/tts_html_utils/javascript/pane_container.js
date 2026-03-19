//pane_container.js

function showPaneById(id) {
  const panes = document.querySelectorAll('[data-id]');

  panes.forEach(pane => {
    pane.classList.remove('visible-pane');
    pane.classList.add('hidden-pane');
    pane.style.display = ''; // Clear inline style if used earlier
  });

  const target = document.querySelector(`[data-id="${id}"]`) || panes[0];
  if (target) {
    target.classList.remove('hidden-pane');
    target.classList.add('visible-pane');
  }
}

function updateUrlHash(id) {
  history.pushState(null, '', `#${id}`); // Updates URL without reloading
}

// Handle nav click
document.addEventListener('click', function (e) {
  if (e.target.matches('[data-nav]')) {
    e.preventDefault();
    const id = e.target.getAttribute('data-nav');
    updateUrlHash(id);
    showPaneById(id);
  }
});

// Handle back/forward navigation
window.addEventListener('popstate', () => {
  const id = window.location.hash.substring(1);
  showPaneById(id);
});

// Show the right pane on initial load
window.addEventListener('DOMContentLoaded', () => {
  const id = window.location.hash.substring(1);
  showPaneById(id);
});