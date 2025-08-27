const input = document.getElementById('activity_level');
const sel = document.getElementById('activity_level_select');

sel.addEventListener('change', () => {
    // copy value from select to input
    if (sel.value) input.value = sel.value;

    // keep select in sync if user later edits input
    input.addEventListener('input', () => {
        const val = (input.value || '').trim();
        sel.value = Array.from(sel.options).some(o => o.value === val) ? val : '';
    });
});
