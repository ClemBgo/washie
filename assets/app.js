(function () {
  var P = window.WS_PRODUCTS || {}, CFG = window.WASHIE_CFG || {};
  var T = window.washieTrack || function () {};
  var mem = [];
  function load() { try { return JSON.parse(localStorage.getItem('washie_cart') || '[]'); } catch (e) { return mem; } }
  function save(c) { mem = c; try { localStorage.setItem('washie_cart', JSON.stringify(c)); } catch (e) {} count(); }
  function eur(v) { return v.toFixed(2).replace('.', ',') + ' €'; }
  function count() { var el = document.getElementById('cart-count'); if (el) el.textContent = load().reduce(function (s, l) { return s + l.qty; }, 0); }
  function variant(pid, vid) { var p = P[pid]; return p.variants.filter(function (x) { return x.id === vid; })[0] || p.variants[0]; }
  function item(pid, v, qty, extra) {
    var p = P[pid], o = {
      item_id: v ? v.id : pid, item_group_id: pid, item_name: p.name, item_brand: 'Washie',
      item_category: p.range, item_category2: p.type,
      item_variant: v ? [v.color, v.size].filter(Boolean).join(' / ') : '',
      price: p.price, quantity: qty || 1
    };
    if (p.list_price > p.price) o.discount = +(p.list_price - p.price).toFixed(2);
    for (var k in extra || {}) o[k] = extra[k];
    return o;
  }
  function ecom(name, items, value, extra) {
    var params = { currency: 'EUR', value: +(value || 0).toFixed(2), items: items };
    for (var k in extra || {}) params[k] = extra[k];
    T(name, params);
  }
  count();

  // Listes de produits (accueil, boutique, recommandations) : view_item_list + select_item
  document.querySelectorAll('[data-list]').forEach(function (list) {
    var name = list.getAttribute('data-list'), items = [];
    list.querySelectorAll('.card').forEach(function (c, i) {
      var pid = c.getAttribute('data-pid');
      if (!P[pid]) return;
      items.push(item(pid, null, 1, { index: i, item_list_name: name }));
      c.querySelectorAll('a').forEach(function (a) {
        a.addEventListener('click', function () { ecom('select_item', [item(pid, null, 1, { index: i, item_list_name: name })], P[pid].price, { item_list_name: name }); });
      });
    });
    if (items.length) ecom('view_item_list', items, 0, { item_list_name: name });
  });

  // CTA, liens guide des tailles, FAQ
  document.querySelectorAll('[data-cta]').forEach(function (a) {
    a.addEventListener('click', function () { T('cta_click', { cta_name: a.getAttribute('data-cta'), cta_text: a.textContent.trim().slice(0, 80) }); });
  });
  document.querySelectorAll('.faq details').forEach(function (d) {
    d.addEventListener('toggle', function () { if (d.open) T('faq_open', { question: d.querySelector('summary').textContent.trim().slice(0, 100) }); });
  });

  // Profondeur de lecture des guides (GEO / contenu)
  if (document.documentElement.getAttribute('data-page-type') === 'guide') {
    var marks = [25, 50, 75, 100], sent = {};
    window.addEventListener('scroll', function () {
      var h = document.documentElement, pct = (h.scrollTop + innerHeight) / h.scrollHeight * 100;
      marks.forEach(function (m) { if (pct >= m && !sent[m]) { sent[m] = 1; T('guide_read', { percent_scrolled: m, guide: location.pathname.split('/').pop() }); } });
    }, { passive: true });
  }

  // Boutique : filtres
  var chips = document.querySelectorAll('.chip');
  if (chips.length) {
    function apply(f, user) {
      chips.forEach(function (c) { c.classList.toggle('on', c.dataset.filter === f); });
      document.querySelectorAll('.shop-sec').forEach(function (s) { s.hidden = !(f === 'all' || s.dataset.range === f); });
      if (user) T('filter_products', { filter_value: f });
    }
    chips.forEach(function (c) { c.addEventListener('click', function () { apply(c.dataset.filter, true); }); });
    var h = (location.hash || '').slice(1);
    if (h && document.querySelector('.shop-sec[data-range="' + h + '"]')) apply(h);
  }

  // Fiche produit
  var pdp = document.querySelector('.pdp');
  if (pdp) {
    var pid = pdp.dataset.product, prod = P[pid], color = (prod.variants[0] || {}).color, sizeSel = document.getElementById('size');
    function current() { var s = sizeSel ? sizeSel.value : ''; return prod.variants.filter(function (v) { return v.color === color && v.size === s; })[0] || prod.variants[0]; }
    function thumbs(v) {
      var t = document.getElementById('thumbs'); t.innerHTML = '';
      [v.image, v.fiche].forEach(function (src, i) {
        var b = document.createElement('button'); b.type = 'button'; b.className = 'th' + (i === 0 ? ' on' : '');
        b.innerHTML = '<img src="' + src + '" alt="" width="90" height="90">';
        b.onclick = function () { document.getElementById('main-img').src = src; t.querySelectorAll('.th').forEach(function (x) { x.classList.remove('on'); }); b.classList.add('on'); T('view_product_image', { image_index: i, item_id: v.id }); };
        t.appendChild(b);
      });
    }
    function show() { var v = current(); document.getElementById('main-img').src = v.image; thumbs(v); var r = document.getElementById('sku'); if (r) r.textContent = v.id; }
    var q = (location.search.match(/[?&]variant=([^&]+)/) || [])[1];
    if (q) {
      var vv = prod.variants.filter(function (v) { return v.id === decodeURIComponent(q); })[0];
      if (vv) {
        color = vv.color; if (sizeSel) sizeSel.value = vv.size;
        document.querySelectorAll('.sw').forEach(function (s) { s.classList.toggle('on', s.dataset.color === color); });
        var cn = document.getElementById('color-name'); if (cn) cn.textContent = color;
      }
    }
    show();
    document.querySelectorAll('.sw').forEach(function (s) {
      s.addEventListener('click', function () {
        color = s.dataset.color;
        document.querySelectorAll('.sw').forEach(function (x) { x.classList.toggle('on', x === s); });
        document.getElementById('color-name').textContent = color; show();
        T('select_variant', { item_id: current().id, variant_type: 'color', variant_value: color });
      });
    });
    if (sizeSel) sizeSel.addEventListener('change', function () { show(); T('select_variant', { item_id: current().id, variant_type: 'size', variant_value: sizeSel.value }); });
    var sg = document.querySelector('[data-size-guide]');
    if (sg) sg.addEventListener('toggle', function () { if (sg.open) T('size_guide_open', { item_group_id: pid }); });
    ecom('view_item', [item(pid, current())], prod.price);
    document.getElementById('add-btn').addEventListener('click', function () {
      var v = current(), qty = Math.max(1, parseInt(document.getElementById('qty').value, 10) || 1), c = load();
      var line = c.filter(function (l) { return l.vid === v.id; })[0];
      if (line) line.qty += qty; else c.push({ pid: pid, vid: v.id, qty: qty });
      save(c); document.getElementById('added').hidden = false;
      ecom('add_to_cart', [item(pid, v, qty)], prod.price * qty);
    });
  }

  // Panier
  var cart = document.getElementById('cart');
  if (cart) {
    var viewed = false;
    function lines() { return load().filter(function (l) { return P[l.pid]; }); }
    function render() {
      var c = lines();
      if (!c.length) { cart.innerHTML = '<p>Votre panier est vide.</p><p><a class="btn" href="boutique.html" data-cta="empty_cart_shop">Voir la boutique</a></p>'; return; }
      var sub = 0, html = '';
      c.forEach(function (l, i) {
        var p = P[l.pid], v = variant(l.pid, l.vid); sub += p.price * l.qty;
        html += '<div class="cart-row"><img src="' + v.image + '" alt="" width="80" height="80"><div><a href="' + p.page + '"><b>' + p.name + '</b></a><br><small>' + [v.color, v.size && ('Taille ' + v.size)].filter(Boolean).join(' · ') + '</small><br><button class="rm" data-i="' + i + '">Retirer</button></div>' +
          '<input type="number" min="1" value="' + l.qty + '" data-i="' + i + '" aria-label="Quantité"><b>' + eur(p.price * l.qty) + '</b></div>';
      });
      var ship = sub >= CFG.freeShip ? 0 : CFG.ship;
      html += '<div class="totals"><span>Sous-total : ' + eur(sub) + '</span><span>Livraison : ' + (ship ? eur(ship) : 'offerte') + '</span>' + (ship ? '<small>Plus que ' + eur(CFG.freeShip - sub) + ' pour la livraison offerte</small>' : '') + '<b>Total : ' + eur(sub + ship) + '</b><button class="btn" id="checkout">Commander</button></div>';
      cart.innerHTML = html;
      cart.querySelectorAll('.rm').forEach(function (b) {
        b.onclick = function () { var c2 = load(), l = c2[+b.dataset.i]; ecom('remove_from_cart', [item(l.pid, variant(l.pid, l.vid), l.qty)], P[l.pid].price * l.qty); c2.splice(+b.dataset.i, 1); save(c2); render(); };
      });
      cart.querySelectorAll('input').forEach(function (inp) {
        inp.onchange = function () { var c2 = load(); c2[+inp.dataset.i].qty = Math.max(1, parseInt(inp.value, 10) || 1); save(c2); render(); };
      });
      var items = c.map(function (l) { return item(l.pid, variant(l.pid, l.vid), l.qty); });
      if (!viewed) { viewed = true; ecom('view_cart', items, sub); }
      document.getElementById('checkout').onclick = function () {
        ecom('begin_checkout', items, sub);
        if (!CFG.ordersOpen) { T('prelaunch_notice', { value: +sub.toFixed(2), currency: 'EUR' }); document.getElementById('prelaunch-modal').hidden = false; }
      };
    }
    render();
    var cm = document.getElementById('close-modal'); if (cm) cm.onclick = function () { document.getElementById('prelaunch-modal').hidden = true; };
  }

  // Formulaires e-mail (liste d'attente / newsletter) – actifs seulement si un endpoint est configuré
  document.querySelectorAll('form[data-lead]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var email = f.querySelector('input[type=email]').value, msg = f.querySelector('.form-msg');
      fetch(CFG.leadEndpoint, { method: 'POST', headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, source: f.getAttribute('data-lead'), page: location.pathname, traffic: (window.WASHIE_TOUCH || {}).session }) })
        .then(function (r) { msg.textContent = r.ok ? 'Merci, c\'est noté !' : 'Une erreur est survenue, réessayez.'; msg.hidden = false; if (r.ok) { T('generate_lead', { lead_source: f.getAttribute('data-lead') }); f.reset(); } })
        .catch(function () { msg.textContent = 'Une erreur est survenue, réessayez.'; msg.hidden = false; });
    });
  });
})();
