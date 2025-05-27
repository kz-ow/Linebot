/* ===== 環境設定 ===== */
const LIFF_ID       = "2007471332-5p2AZlM9";
const POST_ENDPOINT = "/register/language";
/* ================== */

document.addEventListener('DOMContentLoaded', async () => {
  const insideLiff = typeof window.liff !== 'undefined';
  let idToken = null;

  if (insideLiff) {
    await liff.init({ liffId: LIFF_ID });
    await liff.ready;
    idToken = liff.getIDToken() || null;  // ← 再代入
  }

  const radios  = document.querySelectorAll('input[name="lang"]');
  const sendBtn = document.getElementById('sendButton');

  // ラジオは排他的なので、選択有無だけ判定
  radios.forEach(r => r.addEventListener('change', () => {
    sendBtn.disabled = !document.querySelector('input[name="lang"]:checked');
  }));

  sendBtn.addEventListener('click', async () => {
    const chosen = document.querySelector('input[name="lang"]:checked')?.value;
    if (!chosen) return;
    const headers = { 'Content-Type': 'application/json' };
    if (idToken) headers['Authorization'] = `Bearer ${idToken}`;
    
    try {
      const res = await fetch(POST_ENDPOINT, {
        method : 'POST',
        headers: headers,
        cache: 'no-store',
        body   : JSON.stringify({ lang: chosen })
      });

      if (!res.ok) throw new Error('server ' + res.status);
      console.log('POST success');

      if (insideLiff) {
        await liff.closeWindow();
      } else {
        alert('送信しました！');
      }
    } catch (err) {
      console.error('POST failed:', err);
      alert('送信に失敗しました');
    }
  });
});