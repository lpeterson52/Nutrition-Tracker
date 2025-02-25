fetch('./nutritionInfo.json')
    .then(response => response.json())
    .then(data => {
        for (const category in data) {
            for (let i = 0;i<data[category].length;i++) {
                const food = data[category][i];
                const name = food["name"];
                const calories = food["calories"];
                const fat = food["total_fat"];
                const carbs = food["total_carbs"];
                const protein = food["protein"]
                const item = document.createElement('div');
                item.setAttribute('id',name);
                item.innerHTML = name + ", "+calories + ", "+fat +", "+carbs+", "+protein;
                document.body.appendChild(item);
            }
           
        }
    })
    .catch(error => console.error('Error:', error));

