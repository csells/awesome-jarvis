(async () => {
  const select = document.querySelector('#voice');
  const audio = document.querySelector('#voice-sample');
  const detail = document.querySelector('#voice-detail');
  const count = document.querySelector('#voice-count');
  try {
    const response = await fetch('voices.json', {cache:'no-store'});
    if (!response.ok) throw new Error('Could not load the voice catalog');
    const catalog = await response.json();
    const groups = new Map();
    for (const voice of catalog.voices) {
      if (!groups.has(voice.category)) {
        const group = document.createElement('optgroup');
        group.label = voice.category;
        select.append(group); groups.set(voice.category, group);
      }
      const option = document.createElement('option');
      option.value = voice.id; option.textContent = voice.name;
      groups.get(voice.category).append(option);
    }
    function choose() {
      const voice = catalog.voices.find(v => v.id === select.value);
      audio.pause(); audio.removeAttribute('src'); audio.hidden = !voice.sample;
      if (voice.sample) audio.src = voice.sample;
      audio.load();
      detail.textContent = voice.sample_kind;
    }
    select.value = catalog.default;
    select.disabled = false;
    count.textContent = `${catalog.voices.length} voices · ${catalog.voices.filter(v => v.category === 'Pocket built-in voices').length} built-in + ${catalog.voices.filter(v => v.category === 'Custom voices').length} custom`;
    select.addEventListener('change', choose); choose();
    audio.addEventListener('error', () => { detail.textContent = 'The audio sample could not load. Please try again.'; });
  } catch (error) {
    detail.textContent = error.message;
  }
})();
