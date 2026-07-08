(() => {
  const tweets = Array.from(document.querySelectorAll('article[data-testid="tweet"]'));
  const results = [];

  for (const tweet of tweets) {
    try {
      const links = Array.from(tweet.querySelectorAll('div[data-testid="User-Names"] a'));
      const handleLink = links.find(l => l.textContent.includes('@'));
      if (!handleLink) continue;
      const handle = handleLink.textContent.trim();

      const timeEl = tweet.querySelector('time');
      if (!timeEl) continue;
      const timeText = timeEl.textContent;
      const url = timeEl.parentElement.href;

      const textEl = tweet.querySelector('div[data-testid="tweetText"]');
      const text = textEl ? textEl.textContent.trim() : '';

      results.push({ handle, url, text, time: timeText });
    } catch (e) {
      // Skip errors
    }
  }

  return results;
})()