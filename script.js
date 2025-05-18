
        document.addEventListener('DOMContentLoaded', function() {
            // DOM Elements
            const addButton = document.getElementById('addExpense');
            const expenseTableBody = document.getElementById('expenseTableBody');
            const totalBudgetElement = document.getElementById('totalBudget');
            const expenseCountElement = document.getElementById('expenseCount');
            const budgetLimitInput = document.getElementById('budgetLimit');
            const budgetProgress = document.getElementById('budgetProgress');
            const progressBar = document.getElementById('progressBar');
            const budgetMessage = document.getElementById('budgetMessage');
            const currencySelector = document.getElementById('currency');
            const toast = document.getElementById('toast');
            const toastMessage = document.getElementById('toastMessage');
            const loadingSpinner = document.getElementById('loadingSpinner');

            // Sample categories for autocomplete
            const expenseCategories = [
                'Accommodation', 'Flights', 'Transportation', 
                'Food & Dining', 'Activities', 'Shopping',
                'Souvenirs', 'Insurance', 'Visa Fees',
                'Emergency Funds', 'Miscellaneous'
            ];

            // Initialize app
            let expenses = JSON.parse(localStorage.getItem('voyage-expenses')) || [];
            let currency = localStorage.getItem('voyage-currency') || 'USD';
            let tripDetails = JSON.parse(localStorage.getItem('voyage-trip-details')) || {
                name: '',
                destination: '',
                dates: '',
                duration: 7
            };

            // Set initial values from localStorage
            document.getElementById('tripName').value = tripDetails.name;
            document.getElementById('tripDestination').value = tripDetails.destination;
            document.getElementById('tripDates').value = tripDetails.dates;
            document.getElementById('tripDuration').value = tripDetails.duration;
            document.getElementById('budgetLimit').value = tripDetails.budgetLimit || '';
            currencySelector.value = currency;

            // Load existing expenses
            if (expenses.length > 0) {
                renderExpenses();
                calculateTotal();
            }

            // Event Listeners
            addButton.addEventListener('click', addNewExpense);
            budgetLimitInput.addEventListener('input', updateBudgetProgress);
            currencySelector.addEventListener('change', updateCurrency);

            // Save trip details when inputs change
            document.getElementById('tripName').addEventListener('input', saveTripDetails);
            document.getElementById('tripDestination').addEventListener('input', saveTripDetails);
            document.getElementById('tripDates').addEventListener('input', saveTripDetails);
            document.getElementById('tripDuration').addEventListener('input', saveTripDetails);
            budgetLimitInput.addEventListener('input', saveTripDetails);

            // Functions
            function addNewExpense() {
                // Show loading spinner for a better UX
                loadingSpinner.style.display = 'block';
                
                // Simulate async operation (in a real app, this might be an API call)
                setTimeout(() => {
                    const newExpense = {
                        id: Date.now(),
                        category: '',
                        description: '',
                        date: new Date().toISOString().split('T')[0],
                        amount: 0,
                        currency: currency
                    };
                    
                    expenses.push(newExpense);
                    saveExpenses();
                    renderExpenses();
                    
                    // Focus on the first input of the new row
                    const newRow = expenseTableBody.lastElementChild;
                    if (newRow) {
                        const firstInput = newRow.querySelector('input, select');
                        if (firstInput) firstInput.focus();
                    }
                    
                    // Show toast notification
                    showToast('Expense added successfully!');
                    
                    loadingSpinner.style.display = 'none';
                }, 300);
            }

            function renderExpenses() {
                if (expenses.length === 0) {
                    expenseTableBody.innerHTML = `
                        <tr class="empty-state-row">
                            <td colspan="5">
                                <div class="empty-state">
                                    <i class="fas fa-receipt"></i>
                                    <h3>No expenses added yet</h3>
                                    <p>Start by adding your first expense item</p>
                                </div>
                            </td>
                        </tr>
                    `;
                    return;
                }

                expenseTableBody.innerHTML = '';
                
                expenses.forEach((expense, index) => {
                    const row = document.createElement('tr');
                    row.dataset.id = expense.id;
                    row.innerHTML = `
                        <td>
                            <input type="text" class="form-control expense-category" list="categories" value="${expense.category}" placeholder="Select category">
                            <datalist id="categories">
                                ${expenseCategories.map(cat => `<option value="${cat}">`).join('')}
                            </datalist>
                        </td>
                        <td>
                            <input type="text" class="form-control expense-description" value="${expense.description}" placeholder="Brief description">
                        </td>
                        <td>
                            <input type="date" class="form-control expense-date" value="${expense.date}">
                        </td>
                        <td>
                            <div style="display: flex; align-items: center;">
                                <span style="margin-right: 0.5rem;">${getCurrencySymbol()}</span>
                                <input type="number" class="form-control expense-amount" value="${expense.amount}" min="0" step="0.01" placeholder="0.00">
                            </div>
                        </td>
                        <td>
                            <button class="btn btn-danger delete-expense" data-id="${expense.id}">
                                <i class="fas fa-trash-alt btn-icon"></i> Delete
                            </button>
                        </td>
                    `;
                    
                    expenseTableBody.appendChild(row);
                });

                // Add event listeners to all inputs and delete buttons
                document.querySelectorAll('.expense-category').forEach(input => {
                    input.addEventListener('input', updateExpense);
                });
                
                document.querySelectorAll('.expense-description').forEach(input => {
                    input.addEventListener('input', updateExpense);
                });
                
                document.querySelectorAll('.expense-date').forEach(input => {
                    input.addEventListener('input', updateExpense);
                });
                
                document.querySelectorAll('.expense-amount').forEach(input => {
                    input.addEventListener('input', function() {
                        updateExpense.call(this);
                        calculateTotal();
                    });
                });
                
                document.querySelectorAll('.delete-expense').forEach(button => {
                    button.addEventListener('click', deleteExpense);
                });

                // Update expense count
                expenseCountElement.textContent = `${expenses.length} ${expenses.length === 1 ? 'item' : 'items'}`;
            }

            function updateExpense() {
                const row = this.closest('tr');
                const id = parseInt(row.dataset.id);
                const expenseIndex = expenses.findIndex(e => e.id === id);
                
                if (expenseIndex !== -1) {
                    const category = row.querySelector('.expense-category').value;
                    const description = row.querySelector('.expense-description').value;
                    const date = row.querySelector('.expense-date').value;
                    const amount = parseFloat(row.querySelector('.expense-amount').value) || 0;
                    
                    expenses[expenseIndex] = {
                        ...expenses[expenseIndex],
                        category,
                        description,
                        date,
                        amount
                    };
                    
                    saveExpenses();
                }
            }

            function deleteExpense() {
                const id = parseInt(this.dataset.id);
                expenses = expenses.filter(e => e.id !== id);
                saveExpenses();
                renderExpenses();
                calculateTotal();
                showToast('Expense deleted successfully!');
                createConfettiEffect();
            }

            function calculateTotal() {
                let total = 0;
                
                expenses.forEach(expense => {
                    total += parseFloat(expense.amount) || 0;
                });
                
                totalBudgetElement.textContent = `${getCurrencySymbol()}${total.toFixed(2)}`;
                updateBudgetProgress();
                
                // Save expenses as we might have updated amounts
                saveExpenses();
            }

            function updateBudgetProgress() {
                const budgetLimit = parseFloat(budgetLimitInput.value);
                
                if (isNaN(budgetLimit) || budgetLimit <= 0) {
                    budgetProgress.style.display = 'none';
                    budgetMessage.textContent = '';
                    return;
                }
                
                const total = parseFloat(totalBudgetElement.textContent.replace(/[^0-9.]/g, ''));
                const percentage = Math.min((total / budgetLimit) * 100, 100);
                
                budgetProgress.style.display = 'block';
                progressBar.style.width = `${percentage}%`;
                
                // Change color based on percentage
                if (percentage >= 90) {
                    progressBar.style.backgroundColor = 'var(--danger)';
                    budgetMessage.innerHTML = `<i class="fas fa-exclamation-triangle"></i> You're close to your budget limit!`;
                    budgetMessage.style.color = 'var(--danger)';
                } else if (percentage >= 70) {
                    progressBar.style.backgroundColor = 'var(--warning)';
                    budgetMessage.innerHTML = `<i class="fas fa-info-circle"></i> You've used ${Math.round(percentage)}% of your budget`;
                    budgetMessage.style.color = 'var(--warning)';
                } else {
                    progressBar.style.backgroundColor = 'var(--success)';
                    budgetMessage.innerHTML = `<i class="fas fa-check-circle"></i> ${Math.round(100 - percentage)}% of budget remaining`;
                    budgetMessage.style.color = 'var(--success)';
                }
            }

            function updateCurrency() {
                currency = currencySelector.value;
                localStorage.setItem('voyage-currency', currency);
                calculateTotal();
                showToast(`Currency updated to ${currency}`);
            }

            function getCurrencySymbol() {
                switch(currency) {
                    case 'EUR': return '€';
                    case 'GBP': return '£';
                    case 'JPY': return '¥';
                    default: return '$';
                }
            }

            function saveExpenses() {
                localStorage.setItem('voyage-expenses', JSON.stringify(expenses));
            }

            function saveTripDetails() {
                tripDetails = {
                    name: document.getElementById('tripName').value,
                    destination: document.getElementById('tripDestination').value,
                    dates: document.getElementById('tripDates').value,
                    duration: parseInt(document.getElementById('tripDuration').value) || 7,
                    budgetLimit: document.getElementById('budgetLimit').value
                };
                
                localStorage.setItem('voyage-trip-details', JSON.stringify(tripDetails));
            }

            function showToast(message) {
                toastMessage.textContent = message;
                toast.classList.add('show');
                
                setTimeout(() => {
                    toast.classList.remove('show');
                }, 3000);
            }

            function createConfettiEffect() {
                const colors = ['#4361ee', '#3a0ca3', '#4cc9f0', '#7209b7', '#f72585'];
                
                for (let i = 0; i < 50; i++) {
                    const confetti = document.createElement('div');
                    confetti.className = 'confetti';
                    confetti.style.left = Math.random() * 100 + 'vw';
                    confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                    confetti.style.width = Math.random() * 10 + 5 + 'px';
                    confetti.style.height = Math.random() * 10 + 5 + 'px';
                    confetti.style.animationDuration = Math.random() * 3 + 2 + 's';
                    document.body.appendChild(confetti);
                    
                    setTimeout(() => {
                        confetti.remove();
                    }, 5000);
                }
            }

            // Initialize budget progress if there's a limit set
            if (budgetLimitInput.value) {
                updateBudgetProgress();
            }
        });
   