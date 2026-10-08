(() => {
  const body=document.body, theme=document.getElementById('themeBtn'), menu=document.getElementById('menuBtn'), sidebar=document.getElementById('sidebar');
  const saved=localStorage.getItem('scamshield_theme'); if(saved==='light') body.classList.add('light');
  theme?.addEventListener('click',()=>{body.classList.toggle('light');localStorage.setItem('scamshield_theme',body.classList.contains('light')?'light':'dark');theme.textContent=body.classList.contains('light')?'☀':'☾'});
  menu?.addEventListener('click',()=>sidebar?.classList.toggle('open'));
  window.showToast=(msg)=>{const t=document.getElementById('toast');if(!t)return;t.textContent=msg;t.classList.add('show');clearTimeout(window.__toast);window.__toast=setTimeout(()=>t.classList.remove('show'),2600)};
  document.querySelectorAll('[data-toast]').forEach(x=>x.addEventListener('click',()=>showToast(x.dataset.toast)));
  const textarea=document.getElementById('content'), counter=document.getElementById('counter');
  if(textarea&&counter){const update=()=>counter.textContent=`${textarea.value.length} / 5000 characters`;textarea.addEventListener('input',update);update();}
  const typeInput=document.getElementById('input_type');
  document.querySelectorAll('.input-tab').forEach(tab=>tab.addEventListener('click',()=>{document.querySelectorAll('.input-tab').forEach(x=>x.classList.remove('active'));tab.classList.add('active');if(typeInput)typeInput.value=tab.dataset.type;const examples={message:'Paste suspicious SMS, DM or message here...',email:'Paste the email body, sender text and links here...',conversation:'Paste the full conversation here...',url:'Paste a suspicious URL here...'};if(textarea)textarea.placeholder=examples[tab.dataset.type]}));
  const upload=document.getElementById('uploadBtn'), file=document.getElementById('fileInput'); upload?.addEventListener('click',()=>file?.click()); file?.addEventListener('change',async()=>{const f=file.files?.[0];if(!f)return;if(f.size>1024*1024){showToast('File is larger than 1 MB');return;}if(textarea)textarea.value=await f.text();textarea?.dispatchEvent(new Event('input'));showToast(`${f.name} loaded`)});
  const demoText={
    'Banking Scam':'Your bank account will be suspended today. Verify your KYC immediately and send the OTP to customer support.',
    'Job Scam':'Congratulations, your work from home job is approved. Pay the registration fee today to receive your salary.',
    'Lottery Scam':'You have won a lottery prize. Pay a processing fee immediately to claim your reward.',
    'Delivery Scam':'Your parcel is held by customs. Pay the delivery fee now to release your shipment.',
    'Tech Support':'Your computer is infected. Install AnyDesk and give remote access to technical support immediately.',
    'Legitimate':'Hey, are we still meeting tomorrow at 5 PM?'
  };
  document.querySelectorAll('[data-demo]').forEach(btn=>btn.addEventListener('click',()=>{if(textarea){textarea.value=demoText[btn.dataset.demo]||'';textarea.dispatchEvent(new Event('input'));document.getElementById('scanner')?.scrollIntoView({behavior:'smooth',block:'start'});showToast(`${btn.dataset.demo} example loaded`)}}));
  const use=document.getElementById('useExample');use?.addEventListener('click',()=>{if(textarea){textarea.value='Your bank account will be suspended today. Verify your KYC immediately using this link: http://secure-check.example/login';textarea.dispatchEvent(new Event('input'));showToast('Example loaded')}});
})();
