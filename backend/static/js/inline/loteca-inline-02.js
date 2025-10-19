const $ = (id) => {
  const el = document.getElementById(id);
  return (el && el.nodeType === 1) ? el : null;
};
const val = (id, fallback = '') => {
  const el = $(id);
  return el && 'value' in el ? el.value : fallback;
};
// Funções setText e setHTML movidas para loteca-functions.js (implementação oficial)