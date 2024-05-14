document.addEventListener('DOMContentLoaded', () => {
    const userID = parseInt("{{ user_id }}");
    const currentDate = new Date();
    const today = new Date();
    const dayElement = document.getElementById('current-day');
    const prevDayButton = document.getElementById('prev-day');
    const nextDayButton = document.getElementById('next-day');
    const addMealButton = document.getElementById('add-meal-button');
    const removeMealButton = document.getElementById('remove-meal-button');
    const mealForm = document.getElementById('meal-form');
    const removeMealForm = document.getElementById('remove-meal-form');
    const saveMealButton = document.getElementById('save-meal');
    const cancelMealButton = document.getElementById('cancel-meal');
    const cancelRemoveMealButton = document.getElementById('cancel-remove-meal');
    const mealsList = document.getElementById('meals-list');
    const caloriesSumElement = document.getElementById('calories-sum');

    function updateDay() {
        dayElement.textContent = currentDate.toDateString();
        fetchMeals();
        nextDayButton.disabled = currentDate.toDateString() === today.toDateString();
    }

    function fetchMeals() {
        fetch(`/get_diet_data/${currentDate.getFullYear()}/${currentDate.getMonth() + 1}/${currentDate.getDate()}/`)
            .then(response => response.json())
            .then(data => {
                mealsList.innerHTML = '';
                let caloriesSum = 0;
                for (let key in data) {
                    if (data.hasOwnProperty(key)) {
                        const mealRow = document.createElement('tr');
                        const mealNameCell = document.createElement('td');
                        const mealDescriptionCell = document.createElement('td');
                        const mealCaloriesCell = document.createElement('td');

                        mealNameCell.textContent = key.charAt(0).toUpperCase() + key.slice(1);
                        mealDescriptionCell.textContent = data[key].description || 'Brak';
                        mealCaloriesCell.textContent = data[key].calories || 'Brak';

                        mealRow.appendChild(mealNameCell);
                        mealRow.appendChild(mealDescriptionCell);
                        mealRow.appendChild(mealCaloriesCell);

                        mealsList.appendChild(mealRow);

                        caloriesSum += Number(data[key].calories) || 0;
                    }
                }
                caloriesSumElement.textContent = 'Suma kalorii dzisiaj: ' + caloriesSum;
            });
    }

    prevDayButton.addEventListener('click', () => {
        currentDate.setDate(currentDate.getDate() - 1);
        updateDay();
    });

    nextDayButton.addEventListener('click', () => {
        const newDate = new Date(currentDate);
        newDate.setDate(newDate.getDate() + 1);
        if (newDate.toDateString() <= today.toDateString()) {
            currentDate.setDate(currentDate.getDate() + 1);
            updateDay();
        }
    });

    addMealButton.addEventListener('click', () => {
        mealForm.style.display = 'block';
    });

    removeMealButton.addEventListener('click', () => {
        removeMealForm.style.display = 'block';
        mealForm.style.display = 'none';
    });

    saveMealButton.addEventListener('click', (event) => {
        event.preventDefault();

        const mealName = document.getElementById('meal-name').value;
        const mealDescription = document.getElementById('meal-description').value;
        const mealCalories = document.getElementById('meal-calories').value;

        const newMeal = {
            'meal': mealName,
            'description': mealDescription,
            'calories': mealCalories
        };

        fetch(`/post_diet_data/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify(newMeal),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Błąd sieci!');
            }
            return response.json();
        })
        .then(data => {
            console.log('Posiłki zostały zaktualizowane pomyślnie');
            updateDay();
        })
        .catch(error => {
            console.error('Błąd:', error);
        });

        mealForm.style.display = 'none';
    });

    cancelMealButton.addEventListener('click', () => {
        mealForm.style.display = 'none';
    });

    cancelRemoveMealButton.addEventListener('click', () => {
        removeMealForm.style.display = 'none';
    });

    updateDay();
});

// TODO: nie dziala dieta po zmianie z jsona na baze danych trzeba to zmienic, zajme sie tym pozniej