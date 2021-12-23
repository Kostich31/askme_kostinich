// Выбираем все элементы с классом like
const likes = document.querySelectorAll('.like');

// В каждом элементе выбираем плюс и минус. Навешиваем на событие клик функцию render()
likes.forEach(like => {
  const plus = like.querySelector('.plus_btn');
  const minus = like.querySelector('.minus_btn');
  const counter_element = like.querySelector('.counter');
  
  let isLike = 0;
  let counter = counter_element.textContent
  plus.addEventListener('click', () => {
    if(isLike == 0){
      render(++counter, counter_element);
      isLike = -1;
    }
    else if(isLike == -1){
      render(--counter, counter_element);
      isLike = 0;
    }
  });
  
  minus.addEventListener('click', () => {
    if(isLike == 0){
      render(--counter, counter_element);
      isLike = 1;
    }
    else if(isLike == 1){
      render(++counter, counter_element);
      isLike = 0;
    }
  });
});

// Функция обновляет текст
const render = (counter, counter_element) => counter_element.innerText = counter;