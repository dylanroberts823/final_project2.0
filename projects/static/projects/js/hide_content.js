document.addEventListener('click', event => {
  const element = event.target;
  if (element.classList.contains('hide')) {
    element.parentElement.parentElement.style.animationPlayState = 'running';
    element.parentElement.parentElement.addEventListener('animationend', () => {
      element.parentElement.parentElement.remove();
    });
  };
});
