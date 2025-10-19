(() => {
  const NIL = new Proxy(function(){}, {
    get(_, p) {
      if (p === 'value' || p === 'textContent' || p === 'innerHTML') return '';
      return (..._args) => NIL;
    },
    set() { return true; }
  });
  const _get = Document.prototype.getElementById;
  Document.prototype.getElementById = function(id) {
    return _get.call(this, id) || NIL;
  };
})();