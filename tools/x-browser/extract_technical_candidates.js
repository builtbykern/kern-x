(() => {
  const articles = Array.from(document.querySelectorAll('article'));
  const results = [];

  for (const article of articles) {
    try {
      const timeEl = article.querySelector('time');
      if (!timeEl) continue;
      const timeText = timeEl.textContent;
      const url = timeEl.parentElement.href;

      // Last ~4h: "3h", "45m", "20s", "Just now" (not "May 25" day stamps)
      const isRecent = /(?:\d+\s*[hms]|Just now)/i.test(timeText) && !/\d{4}/.test(timeText);
      if (!isRecent) continue;

      const links = Array.from(article.querySelectorAll('a'));
      const handleLink = links.find(l => l.innerText.includes('@'));
      if (!handleLink) continue;
      const handle = handleLink.innerText.trim();
      const rawHandle = handle.replace('@', '').toLowerCase();

      const textEl = article.querySelector('div[data-testid="tweetText"]');
      const text = textEl ? textEl.innerText.trim() : '';

      const lowerText = text.toLowerCase();
      const hasFramer = lowerText.includes('framer');
      const hasCursor = lowerText.includes('cursor') && (lowerText.includes('ai') || lowerText.includes('code') || lowerText.includes('component') || lowerText.includes('editor'));
      const hasMedia = !!article.querySelector('video, [data-testid="tweetPhoto"], [data-testid="videoPlayer"]');
      const craft = ['component', 'motion', 'breakpoint', 'control', 'override', 'canvas', 'marketplace', 'scroll', 'template', 'challenge', 'listing', 'submission', 'shipped', 'published'];
      const hasCraft = craft.some(k => lowerText.includes(k));
      const isChallenge = lowerText.includes('#framerchallenge') || lowerText.includes('framerchallenge');

      if ((hasFramer && (hasMedia || hasCraft || isChallenge)) || hasCursor) {
        results.push({ handle, url, text });
      }
    } catch (e) {}
  }

  // Deduplicate by URL
  const uniqueResults = [];
  const seenUrls = new Set();
  for (const r of results) {
    if (!seenUrls.has(r.url)) {
      seenUrls.add(r.url);
      uniqueResults.push(r);
    }
  }

  return uniqueResults;
})()