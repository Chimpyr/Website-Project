const form = document.querySelector('form');

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const firstName = document.querySelector('input[name="firstName"]').value;
  const lastName = document.querySelector('input[name="lastName"]').value;
  const email = document.querySelector('input[name="email"]').value;
  const password = document.querySelector('input[name="password"]').value;
  const error = document.getElementById('error');


  if (!firstName || !lastName || !email || !password) {
    error.textContent = 'All fields are required';
    return;
  }

  if (!validateEmail(email)) {
    error.textContent = 'Please enter a valid email address';
    return;
  }

  if (!validatePassword(password)) {
    error.textContent = 'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one special character, and one number';
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
