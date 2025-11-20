// ...existing code...
/*
  Scanner with file-upload support.
  - camera scanning (Html5QrcodeScanner)
  - image upload scanning (Html5Qrcode.scanFileV2 via instance)
*/

function normalizeScannedText(text) {
  if (!text) return '';
  text = String(text).trim();
  try {
    if (text.includes('/')) {
      const parts = text.replace(/\/+$/, '').split('/');
      const last = parts.filter(Boolean).pop();
      if (last) return last;
    }
  } catch (e) {}
  return text;
}

async function postUnlock(payload, onSuccess, onError) {
  console.log('POST /api/unlock payload:', payload);
  try {
    const res = await fetch('/api/unlock', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });
    console.log('Response status:', res.status, res.statusText);
    const text = await res.text();
    let json;
    try {
      json = text ? JSON.parse(text) : null;
      console.log('Parsed JSON:', json);
    } catch (e) {
      console.warn('Response not JSON. raw response:', text);
      onError({ msg: `Server returned non-JSON response (status ${res.status})`, raw: text, status: res.status });
      return;
    }
    if (res.ok && json && json.status === 'success') onSuccess(json);
    else onError(json || { msg: 'Unlock failed', status: res.status });
  } catch (err) {
    console.error('Network/fetch error:', err);
    onError({ msg: 'Network error', error: String(err) });
  }
}

/* camera scanner (existing behavior) */
function createCameraScanner() {
  const scanner = new Html5QrcodeScanner("reader", { fps: 10, qrbox: 250 }, false);
  scanner.render((decodedText) => {
    console.log('camera decodedText:', decodedText);
    const normalized = normalizeScannedText(decodedText);
    try { scanner.pause(true); } catch(e){}
    postUnlock({ bike_id: normalized }, (json) => { alert(json.msg || 'Unlocked'); window.location.href = '/dashboard'; },
      (errJson) => { alert(errJson.msg || 'Unlock failed'); console.warn(errJson); try { scanner.resume(); } catch(e){}; });
  }, ()=>{/* frame errors ignored */});
}

/* file-upload scanning */
function initFileScanner() {
  const fileInput = document.getElementById('qr-file');
  const preview = document.getElementById('upload-preview');
  // create html5-qrcode instance bound to the hidden container
  const html5QrForImage = new Html5Qrcode("reader-file");

  fileInput.addEventListener('change', async (ev) => {
    const f = ev.target.files && ev.target.files[0];
    preview.innerHTML = '';
    if (!f) return;
    // preview image
    const img = document.createElement('img');
    img.style.maxWidth = '220px';
    img.style.maxHeight = '220px';
    img.src = URL.createObjectURL(f);
    preview.appendChild(img);

    try {
      // scan image file (scanFileV2 available in html5-qrcode)
      const result = await html5QrForImage.scanFileV2(f, /* showImage= */ true);
      if (result && result.decodedText) {
        console.log('file decodedText:', result.decodedText);
        const normalized = normalizeScannedText(result.decodedText);
        postUnlock({ bike_id: normalized }, (json) => { alert(json.msg || 'Unlocked'); window.location.href = '/dashboard'; },
          (errJson) => { alert(errJson.msg || 'Unlock failed'); console.warn(errJson); });
      } else {
        alert('Could not decode QR from image. Try a clearer/larger image or use camera scan.');
        console.warn('scanFileV2 returned no decodedText:', result);
      }
    } catch (err) {
      console.error('scanFileV2 error:', err);
      alert('Error scanning image. See console for details.');
    } finally {
      try { html5QrForImage.clear(); } catch(e){}
      URL.revokeObjectURL(img.src);
      fileInput.value = '';
    }
  });
}

function initScannerWithPreferredCamera() {
  Html5Qrcode.getCameras().then(cameras => {
    if (!cameras || !cameras.length) { alert('No camera found'); }
    createCameraScanner();
  }).catch(err => {
    console.error('Could not get cameras:', err);
    createCameraScanner();
  });

  initFileScanner();
}

document.addEventListener('DOMContentLoaded', initScannerWithPreferredCamera);
// ...existing code...