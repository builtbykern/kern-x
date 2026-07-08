(() => {
  const articles = Array.from(document.querySelectorAll('article'));
  return articles.map(article => {
    const text = article.innerText || '';
    const link = article.querySelector('time')?.parentElement?.href || '';
    const handle = article.querySelector('a[href^="/"]')?.innerText || '';
    return { handle, link, text: text.substring(0, 100) };
  });
})()