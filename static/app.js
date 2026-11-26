(function () {
  // ----- Toasts: dismiss button + auto-hide success messages -----
  function dismiss(toast) {
    toast.classList.add('hide');
    setTimeout(function () { toast.remove(); }, 300);
  }
  document.querySelectorAll('.toast').forEach(function (toast) {
    toast.querySelector('.toast-close').addEventListener('click', function () { dismiss(toast); });
    if (toast.classList.contains('toast-success')) setTimeout(function () { dismiss(toast); }, 4000);
  });

  // ----- Avatar colours (stable per student id) -----
  var palette = ['#4f46e5', '#0891b2', '#059669', '#d97706', '#db2777', '#7c3aed', '#2563eb', '#dc2626'];
  document.querySelectorAll('.avatar[data-seed]').forEach(function (el) {
    el.style.background = palette[Number(el.dataset.seed) % palette.length];
  });

  // ----- Styled confirm dialog for delete forms -----
  var dialog = null;
  function confirmDialog(message, onConfirm) {
    if (!dialog) {
      dialog = document.createElement('dialog');
      dialog.className = 'confirm';
      dialog.innerHTML =
        '<p></p><div class="row">' +
        '<button type="button" class="btn btn-ghost" data-act="cancel">Cancel</button>' +
        '<button type="button" class="btn btn-danger" data-act="ok">Delete</button></div>';
      document.body.appendChild(dialog);
      dialog.querySelector('[data-act="cancel"]').addEventListener('click', function () { dialog.close(); });
    }
    dialog.querySelector('p').textContent = message;
    var ok = dialog.querySelector('[data-act="ok"]');
    var fresh = ok.cloneNode(true); // drop old listeners
    ok.replaceWith(fresh);
    fresh.addEventListener('click', function () { dialog.close(); onConfirm(); });
    dialog.showModal();
    fresh.focus();
  }
  document.querySelectorAll('form[data-confirm]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      if (form.dataset.confirmed) return;
      e.preventDefault();
      if (typeof HTMLDialogElement === 'undefined') {
        if (window.confirm(form.dataset.confirm)) form.submit();
        return;
      }
      confirmDialog(form.dataset.confirm, function () { form.dataset.confirmed = '1'; form.submit(); });
    });
  });

  // ----- Inline form validation -----
  var form = document.getElementById('studentForm');
  if (!form) return;

  var emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  function check(input) {
    var v = input.value.trim(), msg = '';
    if (input.required && !v) msg = 'This field is required.';
    else if (input.type === 'email' && v && !emailRe.test(v)) msg = 'Enter a valid email address.';
    var field = input.closest('.field');
    field.classList.toggle('invalid', !!msg);
    field.querySelector('.error-text').textContent = msg;
    return !msg;
  }
  var inputs = form.querySelectorAll('input');
  inputs.forEach(function (input) {
    input.addEventListener('blur', function () { check(input); });
    input.addEventListener('input', function () {
      if (input.closest('.field').classList.contains('invalid')) check(input);
    });
  });
  form.addEventListener('submit', function (e) {
    var firstBad = null;
    inputs.forEach(function (input) { if (!check(input) && !firstBad) firstBad = input; });
    if (firstBad) { e.preventDefault(); firstBad.focus(); }
  });
})();
