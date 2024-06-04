document.addEventListener('DOMContentLoaded', () => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  let currentDate = new Date();
  let today = new Date();
  const dayElement = document.getElementById('current-day');
  const prevDayButton = document.getElementById('prev-day');
  const nextDayButton = document.getElementById('next-day');

  function updateDay() {
    dayElement.textContent = currentDate.toLocaleDateString('pl-PL', options);
    nextDayButton.disabled = currentDate.toDateString() === today.toDateString();

    fetch(`/diets/${currentDate.getFullYear()}/${currentDate.getMonth() + 1}/${currentDate.getDate()}/`)
      .then((response) => response.json())
      .then((data) => {
        document.getElementById('meal').value = data.meal || '';
        document.getElementById('description').value = data.description || '';
        document.getElementById('calories').value = data.calories || '';
      });
  }

  prevDayButton.addEventListener('click', () => {
    currentDate.setDate(currentDate.getDate() - 1);
    currentDate = new Date(currentDate);
    updateDay();
  });

  nextDayButton.addEventListener('click', () => {
    const newDate = new Date(currentDate);
    newDate.setDate(newDate.getDate() + 1);
    if (newDate.toDateString() <= today.toDateString()) {
      currentDate.setDate(currentDate.getDate() + 1);
      currentDate = new Date(currentDate);
      updateDay();
    }
  });

  updateDay();

  const editIcons = document.querySelectorAll('.edit-icon');
  editIcons.forEach((icon) => {
    icon.addEventListener('click', (event) => {
      event.preventDefault();
      const inputField = event.target.previousElementSibling;
      inputField.readOnly = !inputField.readOnly;
    });
  });

  const submitButton = document.getElementById('submit-button');
  const inputs = document.querySelectorAll('input');

  inputs.forEach((input) => {
    input.addEventListener('change', () => {
      submitButton.disabled = false;
    });
  });

  document.getElementById('diet-form').addEventListener('submit', (event) => {
    event.preventDefault();

    const data = {
      date: currentDate.toISOString().split('T')[0],
      meal: document.getElementById('meal').value,
      description: document.getElementById('description').value,
      calories: document.getElementById('calories').value,
    };

    fetch(`/post_diets/${currentDate.getFullYear()}/${currentDate.getMonth() + 1}/${currentDate.getDate()}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        const popup = document.getElementById('success-popup');
        popup.style.display = 'block';
        setTimeout(() => {
          popup.style.display = 'none';
        }, 2000);

        updateDay();
      })
      .catch((error) => {
        console.error('Błąd:', error);
      });
  });
});
