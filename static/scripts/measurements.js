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

    fetch(`/measurements/${currentDate.getFullYear()}/${currentDate.getMonth() + 1}/${currentDate.getDate()}/`)
      .then((response) => response.json())
      .then((data) => {
        document.getElementById('chest_circumference').value = data.bust_size || '';
        document.getElementById('weight').value = data.weight || '';
        document.getElementById('height').value = data.height || '';
        document.getElementById('biceps_size').value = data.biceps_size || '';
        document.getElementById('waist_size').value = data.waist_size || '';
        document.getElementById('thighs_size').value = data.thighs_size || '';
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

  document.getElementById('measurement-form').addEventListener('submit', (event) => {
    event.preventDefault();

    const data = {
      date: currentDate.toISOString().split('T')[0],
      height: document.getElementById('height').value,
      weight: document.getElementById('weight').value,
      chest_circumference: document.getElementById('chest_circumference').value,
      biceps_size: document.getElementById('biceps_size').value,
      waist_size: document.getElementById('waist_size').value,
      thighs_size: document.getElementById('thighs_size').value,
    };

    fetch(`/post_measurements/${currentDate.getFullYear()}/${currentDate.getMonth() + 1}/${currentDate.getDate()}/`, {
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
