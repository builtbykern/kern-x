(() => {
  const articles = Array.from(document.querySelectorAll('article'));
  const results = [];

  function within4h(timeText) {
    const t = (timeText || '').trim();
    if (/just now/i.test(t)) return true;
    if (/\d{4}/.test(t) || /\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b/i.test(t)) {
      return false;
    }
    const m = t.match(/(\d+)\s*([dhms])/i);
    if (!m) return false;
    const n = parseInt(m[1], 10);
    const u = m[2].toLowerCase();
    if (u === 's' || u === 'm') return true;
    if (u === 'h') return n <= 4;
    return false; // days
  }

  for (const article of articles) {
    try {
      const timeEl = article.querySelector('time');
      if (!timeEl) continue;
      const timeText = timeEl.textContent || '';
      if (!within4h(timeText)) continue;

      const url = timeEl.parentElement && timeEl.parentElement.href;
      if (!url) continue;

      const links = Array.from(article.querySelectorAll('a'));
      const handleLink = links.find(l => l.innerText && l.innerText.includes('@'));
      if (!handleLink) continue;
      const handle = handleLink.innerText.trim();

      const textEl = article.querySelector('div[data-testid="tweetText"]');
      const text = textEl ? textEl.innerText.trim() : '';

      const lowerText = text.toLowerCase();
      const hasFramer = lowerText.includes('framer');
      const hasCursor =
        lowerText.includes('cursor') &&
        (lowerText.includes('ai') ||
          lowerText.includes('code') ||
          lowerText.includes('component') ||
          lowerText.includes('editor'));
      const hasMedia = !!article.querySelector(
        'video, [data-testid="tweetPhoto"], [data-testid="videoPlayer"], [data-testid="videoComponent"]'
      );
      const craft = [
        'component',
        'motion',
        'breakpoint',
        'control',
        'override',
        'canvas',
        'marketplace',
        'scroll',
        'template',
        'challenge',
        'listing',
        'submission',
        'shipped',
        'published',
      ];
      const hasCraft = craft.some((k) => lowerText.includes(k));
      const isChallenge =
        lowerText.includes('#framerchallenge') || lowerText.includes('framerchallenge');

      if ((hasFramer && (hasMedia || hasCraft || isChallenge)) || hasCursor) {
        results.push({
          handle,
          url,
          text,
          has_media: hasMedia,
          age_label: timeText.trim(),
        });
      }
    } catch (e) {}
  }

  const uniqueResults = [];
  const seenUrls = new Set();
  for (const r of results) {
    if (!seenUrls.has(r.url)) {
      seenUrls.add(r.url);
      uniqueResults.push(r);
    }
  }

  // Media-first within the extract batch
  uniqueResults.sort((a, b) => Number(b.has_media) - Number(a.has_media));

  return uniqueResults;
})()
