// scroll_sync.js

const tableIds{{ uuid }} = {{ table_ids | tojson }};

function syncHorizontalScroll(containers) {
  let isSyncing = false;

  containers.forEach((el, idx) => {
    el.addEventListener('scroll', () => {
      if (isSyncing) return;
      isSyncing = true;
      const scrollLeft = el.scrollLeft;

      containers.forEach((other, otherIdx) => {
        if (other !== el) {
          other.scrollLeft = scrollLeft;
        }
      });

      isSyncing = false;
    });
  });
}

// Example usage:
document.addEventListener('DOMContentLoaded', () => {
  const wrappers = tableIds{{ uuid }}.map(id => document.getElementById(id)).filter(Boolean);
  syncHorizontalScroll(wrappers);
});
