/**
 * prototype-interactions.js — ANTA Prototype Interactivity (v2.1)
 * 
 * PRE-BUILT asset. The AI agent NEVER modifies this file.
 * Agent uses data-* attributes in HTML; this script handles the behavior.
 * 
 * Press ? to toggle Inspector Mode (highlights all interactive elements).
 * 
 * Supported attributes:
 *   data-navigate="./page.html"         → click navigates to URL
 *   data-toggle="#modalId"              → click toggles .anta-visible on target
 *   data-dismiss="modal"               → click hides closest .anta-modal-overlay
 *   data-tab="tabName"                 → click activates tab (within data-tab-group)
 *   data-tab-panel="tabName"           → content panel shown when tab active
 *   data-state-select                  → <select> that drives state visibility
 *   data-show-state="DRAFT"            → element visible only when state matches
 *   data-validate-error                → adds .anta-field-error on parent .anta-form-item
 */

document.addEventListener('DOMContentLoaded', () => {
  // Navigation
  document.querySelectorAll('[data-navigate]').forEach(el =>
    el.addEventListener('click', e => {
      e.preventDefault();
      window.location.href = el.dataset.navigate;
    })
  );

  // Toggle visibility (modals, panels, drawers)
  document.querySelectorAll('[data-toggle]').forEach(el =>
    el.addEventListener('click', e => {
      e.preventDefault();
      const target = document.querySelector(el.dataset.toggle);
      if (target) target.classList.toggle('anta-visible');
    })
  );

  // Dismiss (close modal by clicking cancel/close/X)
  document.querySelectorAll('[data-dismiss="modal"]').forEach(el =>
    el.addEventListener('click', e => {
      e.preventDefault();
      const overlay = el.closest('.anta-modal-overlay');
      if (overlay) overlay.classList.remove('anta-visible');
    })
  );

  // Tabs
  document.querySelectorAll('[data-tab]').forEach(el =>
    el.addEventListener('click', e => {
      e.preventDefault();
      const group = el.closest('[data-tab-group]');
      if (!group) return;
      // Deactivate all tabs + panels
      group.querySelectorAll('[data-tab]').forEach(t => t.classList.remove('anta-tab--active'));
      group.querySelectorAll('[data-tab-panel]').forEach(p => p.classList.remove('anta-visible'));
      // Activate clicked tab + its panel
      el.classList.add('anta-tab--active');
      const panel = group.querySelector('[data-tab-panel="' + el.dataset.tab + '"]');
      if (panel) panel.classList.add('anta-visible');
    })
  );

  // State-driven visibility (workflow state selector)
  document.querySelectorAll('[data-state-select]').forEach(sel => {
    const sync = () => {
      const container = sel.closest('[data-state-container]') || document;
      const val = sel.value;
      container.querySelectorAll('[data-show-state]').forEach(s => {
        s.style.display = s.dataset.showState === val ? '' : 'none';
      });
    };
    sel.addEventListener('change', sync);
    sync(); // initial state
  });

  // Validation error toggle (click to simulate)
  document.querySelectorAll('[data-validate-error]').forEach(el => {
    const item = el.closest('.anta-form-item');
    if (item) item.classList.add('anta-field-error');
  });

  // Initialize: hide all modals (start hidden, toggle shows them)
  document.querySelectorAll('.anta-modal-overlay:not(.anta-visible)').forEach(m => {
    m.style.display = 'none';
  });

  // Observer: sync display with .anta-visible class
  const observer = new MutationObserver(mutations => {
    mutations.forEach(m => {
      if (m.type === 'attributes' && m.attributeName === 'class') {
        const el = m.target;
        if (el.classList.contains('anta-modal-overlay')) {
          el.style.display = el.classList.contains('anta-visible') ? '' : 'none';
        }
      }
    });
  });
  document.querySelectorAll('.anta-modal-overlay').forEach(m =>
    observer.observe(m, { attributes: true })
  );

  // Inspector mode — press ? to highlight all interactive elements and their destinations
  document.addEventListener('keydown', e => {
    if (e.key === '?' && !e.target.matches('input, textarea, select')) {
      document.body.classList.toggle('anta-inspect');
    }
  });
});
