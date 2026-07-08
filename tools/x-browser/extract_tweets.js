(() => {
  const excludedHandles = new Set([
    'iSamyadeep', 'kunal_builds', 'dom_strykowski', 'Error403k', 'dav_pukha', 'faizaneeee', 'max_iriani', 'aandreug', 'theay_o', 'FKThedesigner', 'ashie_designs', 'byaoril', 'aleksihuusko', 'denibozo', 'klm_gfx', 'Rownock_Hasan', 'JedHurricane', '3747Edi', '_miguel_onana', 'jota_fisga', 'PhoenixShawC', 'heykaneriya', 'redwanhrahat', 'denibelx', 'eamin_ux', 'Yousefcopy', 'ZumiStudio_', 'Techpro_06', 'JJGerrishDev', 'ui_varshaa', 'ClarivStudio', 'kadircalik', 'kid_withadream_', 'Matthias_Oel', 'itsanwarraza', 'tilljanek', 'markmhennick', 'TimAkihiro', 'nwldesigns', 'iakanshasoni', 'AnuKrishna_', 'jhicks2306', 'MuhamadAbubaker', 'pushrefresh', 'itszineddine', 'BuiltWithBala'
  ].map(h => h.toLowerCase().replace('@', '')));

  const tweets = Array.from(document.querySelectorAll('article[data-testid="tweet"]'));
  const results = [];

  for (const tweet of tweets) {
    try {
      const handleEl = tweet.querySelector('div[data-testid="User-Names"] a[href^="/"] div > span');
      // Wait, handle is usually the second link or has @.
      const links = Array.from(tweet.querySelectorAll('div[data-testid="User-Names"] a[href^="/"]'));
      const handleLink = links.find(l => l.textContent.includes('@'));
      if (!handleLink) continue;
      const handle = handleLink.textContent.trim();
      const rawHandle = handle.replace('@', '').toLowerCase();

      if (excludedHandles.has(rawHandle)) continue;

      const timeEl = tweet.querySelector('time');
      if (!timeEl) continue;
      const timeText = timeEl.textContent;
      const url = timeEl.parentElement.href;

      // Check if within 24h: "h", "m", "s", or "Just now".
      // "May 18" might be within 24h depending on the current time.
      // But "May 17" is definitely not.
      const isRecent = /h|m|s|Just now/.test(timeText) || (timeText.includes('May 18') && !timeText.includes('2025'));

      if (!isRecent) continue;

      const textEl = tweet.querySelector('div[data-testid="tweetText"]');
      if (!textEl) continue;
      const text = textEl.textContent.trim();

      const lowerText = text.toLowerCase();
      const isTechnical = (lowerText.includes('component') || lowerText.includes('override') || lowerText.includes('custom')) && lowerText.includes('framer');

      if (isTechnical) {
        results.push({ handle, url, text });
      }
    } catch (e) {
      // Skip errors
    }
  }

  return results;
})()