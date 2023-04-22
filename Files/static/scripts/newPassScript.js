const form = document.querySelector('form');
const error = document.getElementById('error');

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const email = document.querySelector('input[name="email"]').value;
  const oldPassword = document.querySelector('input[name="old_password"]').value;
  const newPassword = document.querySelector('input[name="new_password"]').value;
  const confirmNewPassword = document.querySelector('input[name="confirm_new_password"]').value;

  if (!email || !oldPassword || !newPassword || !confirmNewPassword) {
    error.textContent = 'All fields are required';
    return;
  }

  if (!validateEmail(email)) {
    error.textContent = 'Please enter a valid email address';
    return;
  }

  if (newPassword !== confirmNewPassword) {
    error.textContent = 'Passwords do not match';
    return;
  }

  if (!validatePassword(newPassword)) {
    error.textContent = 'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number';
    return;
  }

  form.submit();
});

function validateEmail(email) {
  const re = /\S+@\S+\.\S+/;
  return re.test(String(email).toLowerCase());
}

function validatePassword(password) {
  const re = /^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
  return re.test(password);
}
