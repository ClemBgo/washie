/* Washie – consentement, attribution et Google Analytics 4.
   Chargé dans le <head>, avant toute autre balise. */
(function () {
  var C = window.WASHIE_CFG || {};
  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = gtag;

  function lsGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function ssGet(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }
  function ssSet(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }

  // 1. Consent Mode v2 : tout refusé par défaut (RGPD / CNIL), mis à jour par la bannière
  var stored = lsGet('washie_consent');
  gtag('consent', 'default', {
    ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied',
    analytics_storage: 'denied', functionality_storage: 'granted', security_storage: 'granted',
    wait_for_update: 500
  });
  gtag('set', 'ads_data_redaction', true);
  gtag('set', 'url_passthrough', true);
  if (stored === 'granted') {
    gtag('consent', 'update', { ad_storage: 'granted', ad_user_data: 'granted', ad_personalization: 'granted', analytics_storage: 'granted' });
  }

  // 2. Attribution : classe chaque session en payant / organique / IA / social / e-mail / referral / direct
  var q = new URLSearchParams(location.search);
  var ref = document.referrer || '';
  var refHost = '';
  try { refHost = ref ? new URL(ref).hostname.replace(/^www\./, '') : ''; } catch (e) {}
  var ownHost = location.hostname.replace(/^www\./, '');
  var internal = refHost && refHost === ownHost;

  function classify() {
    var src = (q.get('utm_source') || '').toLowerCase();
    var med = (q.get('utm_medium') || '').toLowerCase();
    var camp = q.get('utm_campaign') || '';
    var clickId = ['gclid', 'gbraid', 'wbraid', 'msclkid', 'fbclid', 'ttclid', 'li_fat_id', 'epik', 'sccid'].filter(function (k) { return q.get(k); })[0];
    var ai = /(chatgpt\.com|chat\.openai\.com|openai\.com|perplexity\.ai|claude\.ai|gemini\.google\.com|bard\.google\.com|copilot\.microsoft\.com|you\.com|phind\.com|poe\.com|mistral\.ai|chat\.mistral\.ai|deepseek\.com|meta\.ai|grok\.com)/;
    var search = /(^|\.)(google\.[a-z.]+|bing\.com|duckduckgo\.com|qwant\.com|ecosia\.org|yahoo\.[a-z.]+|search\.brave\.com|startpage\.com|lilo\.org|yandex\.[a-z.]+|baidu\.com)$/;
    var social = /(facebook\.com|instagram\.com|l\.instagram\.com|m\.facebook\.com|lm\.facebook\.com|t\.co|twitter\.com|x\.com|linkedin\.com|lnkd\.in|pinterest\.[a-z.]+|tiktok\.com|youtube\.com|reddit\.com|snapchat\.com|threads\.net)/;
    var t = 'direct', s = '(direct)';
    if (clickId || /^(cpc|ppc|paid|paidsearch|paid_search|paid-social|paid_social|paidsocial|display|cpm|cpv|retargeting|shopping|pmax)/.test(med)) {
      t = 'paid';
      s = src || ({ gclid: 'google', gbraid: 'google', wbraid: 'google', msclkid: 'bing', fbclid: 'meta', ttclid: 'tiktok', li_fat_id: 'linkedin', epik: 'pinterest', sccid: 'snapchat' }[clickId] || 'paid');
      if (clickId === 'fbclid' && !med) { t = 'organic_social'; } // fbclid seul = clic organique Facebook/Instagram
    } else if (ai.test(src) || ai.test(refHost)) {
      t = 'ai_assistant'; s = src || refHost;
    } else if (med === 'email' || med === 'newsletter') {
      t = 'email'; s = src || 'email';
    } else if (med === 'social' || med === 'organic_social' || (!med && social.test(refHost))) {
      t = 'organic_social'; s = src || refHost;
    } else if (med === 'organic' || (!med && search.test(refHost))) {
      t = 'organic_search'; s = src || refHost;
    } else if (med === 'referral' || (refHost && !internal)) {
      t = 'referral'; s = src || refHost;
    } else if (src) {
      t = med || 'other'; s = src;
    }
    return { traffic_type: t, traffic_source: s, traffic_medium: med || '(none)', traffic_campaign: camp || '(not set)', landing_page: location.pathname };
  }

  var session = null;
  try { session = JSON.parse(ssGet('washie_touch') || 'null'); } catch (e) {}
  var isNewTouch = !session || (!internal && (q.get('utm_source') || q.get('gclid') || q.get('gbraid') || q.get('wbraid') || q.get('msclkid') || q.get('fbclid')));
  if (isNewTouch) { session = classify(); ssSet('washie_touch', JSON.stringify(session)); }
  var first = null;
  try { first = JSON.parse(lsGet('washie_first_touch') || 'null'); } catch (e) {}
  if (!first) { first = session; lsSet('washie_first_touch', JSON.stringify(first)); }
  window.WASHIE_TOUCH = { session: session, first: first };

  // 3. Paramètres envoyés avec CHAQUE événement GA4
  var pageType = document.documentElement.getAttribute('data-page-type') || 'other';
  gtag('set', {
    page_type: pageType,
    content_group: pageType,
    traffic_type: session.traffic_type,
    traffic_source: session.traffic_source,
    landing_page: session.landing_page
  });
  gtag('set', 'user_properties', {
    first_traffic_type: first.traffic_type,
    first_traffic_source: first.traffic_source
  });

  // 4. Chargement GA4 / Google Ads
  if (C.ga4) {
    var s = document.createElement('script');
    s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + C.ga4;
    document.head.appendChild(s);
    gtag('js', new Date());
    gtag('config', C.ga4, { page_type: pageType, debug_mode: /[?&]debug=1/.test(location.search) });
    if (C.ads) gtag('config', C.ads);
  }

  // 5. API de suivi utilisée par app.js
  window.washieTrack = function (name, params) {
    params = params || {};
    gtag('event', name, params);
  };

  // 6. Bannière cookies
  window.washieConsent = function (granted) {
    lsSet('washie_consent', granted ? 'granted' : 'denied');
    var v = granted ? 'granted' : 'denied';
    gtag('consent', 'update', { ad_storage: v, ad_user_data: v, ad_personalization: v, analytics_storage: v });
    var b = document.getElementById('cookie-banner'); if (b) b.hidden = true;
    gtag('event', 'consent_choice', { consent: v });
  };
  window.washieShowConsent = function () { var b = document.getElementById('cookie-banner'); if (b) b.hidden = false; };
  document.addEventListener('DOMContentLoaded', function () {
    if (!stored) window.washieShowConsent();
  });
})();
