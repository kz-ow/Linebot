/* ===== 環境設定 ===== */
const LIFF_ID       = "__LIFF_ID__";      // build 時に置換
const POST_ENDPOINT = "/register/mode";    // 相対 or 絶対 URL
/* ================== */

document.addEventListener('DOMContentLoaded', async () => {
  const insideLiff = typeof window.liff !== 'undefined';
  let idToken = null;

  if (insideLiff) {
    await liff.init({ liffId: LIFF_ID });
    await liff.ready;
    idToken = liff.getIDToken() || null;
  }

  const radios = document.querySelectorAll('input[name="mode"]');
  const sendBtn = document.getElementById('sendButton');

  // ラジオは排他的なので、選択有無だけ判定
  radios.forEach(r => r.addEventListener('change', () => {
    sendBtn.disabled = !document.querySelector('input[name="mode"]:checked');
  }));

  // 送信処理
  sendBtn.addEventListener('click', async () => {
    const chosen = document.querySelector('input[name="mode"]:checked')?.value;
    if (!chosen) return;

    const headers = { 'Content-Type': 'application/json' };
    if (idToken) headers['Authorization'] = `Bearer ${idToken}`;

    try {
      const res = await fetch(POST_ENDPOINT, {
        method : 'POST',
        headers: headers,
        body   : JSON.stringify({ mode: chosen })
      });
      if (!res.ok) throw new Error('server ' + res.status);

      if (insideLiff) {
        await liff.closeWindow();
      } else {
        alert('送信しました！');
      }
    } catch (err) {
      console.error(err);
      alert('送信に失敗しました');
    }
  });
});