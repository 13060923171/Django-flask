const container = document.getElementById('container');
const text = document.getElementById('text');

const totalTime = 10000;
const breatheTime = (totalTime / 5);
const holdTime = totalTime / 5;

breathAnimation();

function breathAnimation() {
  text.innerText = '两个人在一起，最重要的感觉就是舒服';
  container.className = 'container grow';

  setTimeout(() => {
    text.innerText = '即使默默不语，也是一种默契';

    setTimeout(() => {
      text.innerText = '纵然两两相望，也是一种欣喜';
      container.className = 'container shrink';
    }, holdTime);
  }, breatheTime);
}

setInterval(breathAnimation, totalTime);
