function login_appear() {
  const login_form = document.querySelect(".login-form");
  body.style.animationPlayState = 'running'
  login_form.style.animationPlayState = 'running';

  if (element.classList.contains('hide')) {
    element.parentElement.parentElement.style.animationPlayState = 'running';
    element.parentElement.parentElement.addEventListener('animationend', () => {
      element.parentElement.parentElement.remove();
    });
  };
};
