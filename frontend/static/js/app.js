// Client-side Application Logic for Weekly Diet Planner
document.addEventListener('DOMContentLoaded', () => {
    const mainLayout = document.querySelector('.main-layout');
    const dietForm = document.getElementById('diet-form');
    const submitBtn = document.getElementById('submit-btn');
    const placeholderView = document.getElementById('placeholder-view');
    const loader = document.getElementById('loader');
    const resultsView = document.getElementById('results-view');
    const aiSection = document.getElementById('ai-section');
    const aiContentBody = document.getElementById('ai-content-body');
    const tabButtons = document.querySelectorAll('.tab-btn');
    
    // Initialize homepage with form-mode
    mainLayout.classList.add('form-mode');
    
    let macroChartInstance = null;
    
    // Memory cache for weekly plan data
    let currentWeeklyPlan = null;
    let currentWeeklyActuals = null;
    let currentMacroTargets = null;
    let currentActiveDay = 'Monday';

    // Handle Form Submit
    dietForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Switch to results view layout
        mainLayout.classList.remove('form-mode');
        mainLayout.classList.add('results-mode');
        
        // Show loader and hide content
        placeholderView.classList.add('hidden');
        resultsView.classList.add('hidden');
        loader.classList.remove('hidden');
        
        // Disable submit button
        submitBtn.disabled = true;
        submitBtn.querySelector('span').innerText = 'Generating Plan...';

        // Extract Form Data
        const formData = new FormData(dietForm);
        const payload = {
            age: formData.get('age'),
            gender: formData.get('gender'),
            height: formData.get('height'),
            weight: formData.get('weight'),
            activity: formData.get('activity'),
            goal: formData.get('goal'),
            diet_pref: formData.get('diet_pref')
        };

        try {
            // POST request to backend API
            const response = await fetch('/api/plan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Server returned an error.');
            }

            const data = await response.json();
            
            if (data.status === 'success') {
                // Cache data globally in script
                currentWeeklyPlan = data.weekly_plan;
                currentWeeklyActuals = data.weekly_actual_totals;
                currentMacroTargets = data.macro_targets;
                
                // Reset to Monday tab on fresh submission
                currentActiveDay = 'Monday';
                setActiveTab(currentActiveDay);
                
                // Populate general static metrics
                document.getElementById('display-calories').innerText = data.target_calories;
                document.getElementById('display-bmi').innerText = data.bmi;
                
                const bmiStatusEl = document.getElementById('display-bmi-status');
                bmiStatusEl.innerText = data.bmi_status;
                bmiStatusEl.className = 'metric-status'; // Reset classes
                const status = data.bmi_status.toLowerCase();
                if (status.includes('normal')) {
                    bmiStatusEl.classList.add('status-normal');
                } else if (status.includes('overweight') || status.includes('underweight')) {
                    bmiStatusEl.classList.add('status-warning');
                } else {
                    bmiStatusEl.classList.add('status-danger');
                }

                // Render targets in text breakdown (stays static)
                document.getElementById('target-protein').innerText = data.macro_targets.protein;
                document.getElementById('target-carbs').innerText = data.macro_targets.carbs;
                document.getElementById('target-fat').innerText = data.macro_targets.fat;

                // Handle AI Coaching response (rendered once for the whole week)
                if (data.ai_coaching) {
                    aiSection.classList.remove('hidden');
                    aiContentBody.innerHTML = marked.parse(data.ai_coaching);
                } else {
                    aiSection.classList.add('hidden');
                    aiContentBody.innerHTML = '';
                }

                // Load active day's visual details
                updateDayUI(currentActiveDay);

                // Show Results panel
                resultsView.classList.remove('hidden');
            } else {
                alert('Failed to generate weekly diet plan. Please try again.');
                resetUI();
            }

        } catch (error) {
            console.error('Error:', error);
            alert(`An error occurred: ${error.message}`);
            resetUI();
        } finally {
            // Hide loader
            loader.classList.add('hidden');
            // Re-enable submit button
            submitBtn.disabled = false;
            submitBtn.querySelector('span').innerText = 'Generate Weekly Plan';
        }
    });

    // Reset UI to placeholder state
    function resetUI() {
        mainLayout.classList.remove('results-mode');
        mainLayout.classList.add('form-mode');
        placeholderView.classList.remove('hidden');
        resultsView.classList.add('hidden');
        loader.classList.add('hidden');
        currentWeeklyPlan = null;
        currentWeeklyActuals = null;
        currentMacroTargets = null;
    }

    // Handle Edit Profile button click to return to the input form
    const editProfileBtn = document.getElementById('edit-profile-btn');
    if (editProfileBtn) {
        editProfileBtn.addEventListener('click', () => {
            mainLayout.classList.remove('results-mode');
            mainLayout.classList.add('form-mode');
        });
    }

    // Set styling of the clicked tab
    function setActiveTab(dayName) {
        tabButtons.forEach(btn => {
            if (btn.dataset.day === dayName) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    }

    // Handle day selection tab click
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            if (!currentWeeklyPlan) return;
            const selectedDay = btn.dataset.day;
            currentActiveDay = selectedDay;
            setActiveTab(selectedDay);
            updateDayUI(selectedDay);
        });
    });

    // Update daily changing UI components (Meal cards, Charts, Actual macros)
    function updateDayUI(day) {
        if (!currentWeeklyPlan || !currentWeeklyPlan[day]) return;

        const dayPlan = currentWeeklyPlan[day];
        const dayActuals = currentWeeklyActuals[day];

        // 1. Update day labels
        document.getElementById('active-day-label').innerText = day;
        document.getElementById('active-day-title').innerText = day;

        // 2. Update daily calorie card actual value
        document.getElementById('display-actual-calories').innerText = `${dayActuals.calories} kcal`;

        // 3. Update actual macros text breakdown
        document.getElementById('actual-protein').innerText = dayActuals.protein;
        document.getElementById('actual-carbs').innerText = dayActuals.carbs;
        document.getElementById('actual-fat').innerText = dayActuals.fat;

        // 4. Update the 4 meal cards
        const meals = ['breakfast', 'lunch', 'snack', 'dinner'];
        meals.forEach(meal => {
            const mealData = dayPlan[meal];
            if (mealData) {
                document.getElementById(`${meal}-name`).innerText = mealData.name;
                document.getElementById(`${meal}-portion`).innerText = mealData.portion_g;
                document.getElementById(`${meal}-calories`).innerText = `${mealData.calories} kcal`;
                document.getElementById(`${meal}-p`).innerText = mealData.protein;
                document.getElementById(`${meal}-c`).innerText = mealData.carbs;
                document.getElementById(`${meal}-f`).innerText = mealData.fat;
            }
        });

        // 5. Draw/Update Chart comparison
        renderChart(currentMacroTargets, dayActuals);
    }

    // Render/re-draw comparison Chart using Chart.js
    function renderChart(targets, actuals) {
        const ctx = document.getElementById('macroChart').getContext('2d');

        // Destroy previous chart instance if exists
        if (macroChartInstance) {
            macroChartInstance.destroy();
        }

        // Create new grouped bar chart
        macroChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Protein (g)', 'Carbs (g)', 'Fat (g)'],
                datasets: [
                    {
                        label: 'Target Goal',
                        data: [targets.protein, targets.carbs, targets.fat],
                        backgroundColor: 'rgba(255, 255, 255, 0.15)',
                        borderColor: 'rgba(255, 255, 255, 0.4)',
                        borderWidth: 1.5,
                        borderRadius: 6,
                        barPercentage: 0.6,
                        categoryPercentage: 0.8
                    },
                    {
                        label: 'Selected Day Plan',
                        data: [actuals.protein, actuals.carbs, actuals.fat],
                        backgroundColor: [
                            'rgba(22, 163, 74, 0.85)', // Protein Green
                            'rgba(30, 136, 229, 0.85)', // Carbs Blue
                            'rgba(234, 88, 12, 0.85)'  // Fat Orange
                        ],
                        borderColor: [
                            'rgb(22, 163, 74)',
                            'rgb(30, 136, 229)',
                            'rgb(234, 88, 12)'
                        ],
                        borderWidth: 1.5,
                        borderRadius: 6,
                        barPercentage: 0.6,
                        categoryPercentage: 0.8
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#a0a8c0',
                            font: {
                                family: 'Inter',
                                size: 11
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return ` ${context.dataset.label}: ${context.raw}g`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#a0a8c0',
                            font: {
                                family: 'Inter',
                                size: 11
                            }
                        }
                    },
                    y: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        },
                        ticks: {
                            color: '#a0a8c0',
                            font: {
                                family: 'Inter',
                                size: 11
                            }
                        }
                    }
                }
            }
        });
    }
});
