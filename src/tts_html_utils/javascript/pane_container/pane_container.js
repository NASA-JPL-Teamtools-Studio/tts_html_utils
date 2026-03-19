//pane_container.js

function showPaneById(id, containerId) {
  // Get the container element
  const container = document.querySelector(`[data-container-id="${containerId}"]`);
  if (!container) return;
  
  // Get all panes that belong to this container
  const panes = container.querySelectorAll('[data-id]');
  
  // Get all nav links in this container's navbar
  const navbar = container.querySelector('ul.navbar');
  if (!navbar) return;
  const navLinks = navbar.querySelectorAll('li.navbartab > a');

  // Hide all panes in this container
  panes.forEach(pane => {
    // Only affect panes that belong to this container
    if (pane.getAttribute('data-container-id') === containerId) {
      pane.classList.remove('visible-pane');
      pane.classList.add('hidden-pane');
      pane.style.display = ''; // Clear inline style if used earlier
    }
  });

  // Remove 'navbartab-active' from all li.navbartab elements in this navbar
  navLinks.forEach(link => {
    const li = link.closest('li.navbartab');
    if (li) {
      li.classList.remove('navbartab-active');
    }
  });

  // Show the target pane
  const target = container.querySelector(`[data-id="${id}"]`);
  if (target) {
    target.classList.remove('hidden-pane');
    target.classList.add('visible-pane');
  }

  // Find the corresponding link by href and mark its parent <li> as active
  const activeLink = navbar.querySelector(`li.navbartab > a[href="#${id}"]`);
  if (activeLink) {
    const activeLi = activeLink.closest('li.navbartab');
    if (activeLi) {
      activeLi.classList.add('navbartab-active');
    }
  }
}

function updateUrlHash(id) {
  history.pushState(null, '', `#${id}`); // Updates URL without reloading
}

// Extract container ID from an element or its ancestors
function getContainerId(element) {
  // First check if the element itself has a container ID
  let containerId = element.getAttribute('data-container-id');
  if (containerId) return containerId;
  
  // Otherwise, look for the closest ancestor with a container ID
  const container = element.closest('[data-container-id]');
  return container ? container.getAttribute('data-container-id') : null;
}

// Handle nav click
document.addEventListener('click', function (e) {
  if (e.target.matches('[data-nav]')) {
    e.preventDefault();
    const id = e.target.getAttribute('data-nav');
    const containerId = getContainerId(e.target);
    if (containerId) {
      updateUrlHash(id);
      showPaneById(id, containerId);
    }
  } else if (e.target.matches('ul.navbar li.navbartab > a')) {
    e.preventDefault();
    const hash = e.target.getAttribute('href');
    const id = hash.startsWith('#') ? hash.slice(1) : hash;
    const containerId = getContainerId(e.target);
    if (containerId) {
      updateUrlHash(id);
      showPaneById(id, containerId);
    }
  }
});

// Initialize all pane containers
function initPaneContainers() {
  // Find all pane containers
  const containers = document.querySelectorAll('.pane-container');
  
  // Initialize each container
  containers.forEach(container => {
    const containerId = container.getAttribute('data-container-id');
    if (!containerId) return;
    
    // Find the first pane in this container
    const firstPane = container.querySelector('[data-id]');
    if (firstPane) {
      const paneId = firstPane.getAttribute('data-id');
      // Show the first pane
      showPaneById(paneId, containerId);
    }
  });
}

// Show the right pane on initial load
window.addEventListener('DOMContentLoaded', () => {
  initPaneContainers();
  
  // Handle URL hash if present
  const hash = window.location.hash;
  if (hash) {
    const id = hash.substring(1);
    // Find the container that has this pane
    const pane = document.querySelector(`[data-id="${id}"]`);
    if (pane) {
      const containerId = pane.getAttribute('data-container-id');
      if (containerId) {
        showPaneById(id, containerId);
      }
    }
  }
});

// Handle back/forward navigation
window.addEventListener('popstate', () => {
  const hash = window.location.hash;
  if (hash) {
    const id = hash.substring(1);
    // Find the container that has this pane
    const pane = document.querySelector(`[data-id="${id}"]`);
    if (pane) {
      const containerId = pane.getAttribute('data-container-id');
      if (containerId) {
        showPaneById(id, containerId);
      }
    }
  }
});
