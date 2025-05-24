/* ===== 環境設定 ===== */
const LIFF_ID       = "__LIFF_ID__";      // build 時に置換
const POST_ENDPOINT = "/register/scheduler";    // 相対 or 絶対 URL
/* ================== */

document.addEventListener('DOMContentLoaded', async () => {
  const insideLiff = typeof window.liff !== 'undefined';
  let idToken = null;

  if (insideLiff) {
    await liff.init({ liffId: LIFF_ID });
    await liff.ready;
    idToken = liff.getIDToken();
  }

  const radios = document.querySelectorAll('input[name="scheduler"]');
  const urlInputContainer = document.getElementById('urlInputContainer');
  const urlInput = document.getElementById('endpointUrl');
  const sendBtn = document.getElementById('sendButton');

  // ボタン活性化判定関数
  function updateSendBtnState() {
    const chosen = document.querySelector('input[name="scheduler"]:checked')?.value;
    if (chosen === 'OFF') {
      sendBtn.disabled = false;
    } else if (chosen === 'ON') {
      const url = urlInput.value.trim();
      // https:// で始まるもののみ有効
      sendBtn.disabled = !(url && url.startsWith('https://'));
    } else {
      sendBtn.disabled = true;
    }
  }

  // 初期状態チェック
  updateSendBtnState();

  // ラジオ選択時の挙動
  radios.forEach(radio => radio.addEventListener('change', () => {
    if (radio.value === 'ON' && radio.checked) {
      urlInputContainer.classList.remove('hidden');
    } else if (radio.value === 'OFF' && radio.checked) {
      urlInputContainer.classList.add('hidden');
    }
    updateSendBtnState();
  }));

  // URL入力時にもボタン状態を更新
  urlInput.addEventListener('input', updateSendBtnState);

  // 送信処理
  sendBtn.addEventListener('click', async () => {
    const chosen = document.querySelector('input[name="scheduler"]:checked')?.value;
    if (!chosen) return;

    const headers = { 'Content-Type': 'application/json' };
    if (idToken) headers['Authorization'] = `Bearer ${idToken}`;

    const payload = { scheduler: chosen };
    if (chosen === 'ON') payload.endpointUrl = urlInput.value.trim();

    try {
      const res = await fetch(POST_ENDPOINT, {
        method : 'POST',
        headers: headers,
        body   : JSON.stringify(payload)
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