(() => {
  const excludedHandles = new Set([
    'iSamyadeep', 'kunal_builds', 'dom_strykowski', 'Error403k', 'dav_pukha', 'faizaneeee', 'max_iriani', 'aandreug', 'theay_o', 'FKThedesigner', 'ashie_designs', 'byaoril', 'aleksihuusko', 'denibozo', 'klm_gfx', 'Rownock_Hasan', 'JedHurricane', '3747Edi', '_miguel_onana', 'jota_fisga', 'PhoenixShawC', 'heykaneriya', 'redwanhrahat', 'denibelx', 'eamin_ux', 'Yousefcopy', 'ZumiStudio_', 'Techpro_06', 'JJGerrishDev', 'ui_varshaa', 'ClarivStudio', 'kadircalik', 'kid_withadream_', 'Matthias_Oel', 'itsanwarraza', 'tilljanek', 'markmhennick', 'TimAkihiro', 'nwldesigns', 'iakanshasoni', 'AnuKrishna_', 'jhicks2306', 'MuhamadAbubaker', 'pushrefresh', 'itszineddine', 'BuiltWithBala'
  ].map(h => h.toLowerCase().replace('@', '')));

  const articles = Array.from(document.querySelectorAll('article'));
  const results = [];

  for (const article of articles) {
    try {
      const timeEl = article.querySelector('time');
      if (!timeEl) continue;
      const timeText = timeEl.textContent;
      const url = timeEl.parentElement.href;

      const isRecent = /h|m|s|Just now/.test(timeText) || (timeText.includes('May 18') && !timeText.includes('2025'));
      if (!isRecent) continue;

      const links = Array.from(article.querySelectorAll('a'));
      const handleLink = links.find(l => l.innerText.includes('@'));
      if (!handleLink) continue;
      const handle = handleLink.innerText.trim();
      const rawHandle = handle.replace('@', '').toLowerCase();

      if (excludedHandles.has(rawHandle)) continue;

      const textEl = article.querySelector('div[data-testid="tweetText"]');
      const text = textEl ? textEl.innerText.trim() : '';

      results.push({ handle, url, text, time: timeText });
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

  return uniqueResults;
})()