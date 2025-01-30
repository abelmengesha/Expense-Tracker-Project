document.addEventListener('DOMContentLoaded', () => {
    // Get the canvas element for the weekly chart
    const ctx = document.getElementById('weeklyChart').getContext('2d');

    // Check if weeklyChartData is available
    if (typeof weeklyChartData !== 'undefined') {
        const { labels, income, expense } = weeklyChartData;

        // Create the bar chart
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels, // Days of the week
                datasets: [
                    {
                        label: 'Income',
                        data: income,
                        backgroundColor: 'rgba(0, 255, 21, 0.6)',
                        borderColor:  'rgba(0, 255, 21, 0.6)',
                        borderWidth: 0.5
                    },
                    {
                        label: 'Expense',
                        data: expense,
                        backgroundColor: 'rgba(255, 0, 106, 0.6)',
                        borderColor: 'rgba(255, 0, 0, 0.6)',
                        borderWidth: 0.5
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false, // Allow the chart to adjust size responsively
                plugins: {
                    title: {
                        display: true,
                        text: 'Weekly Income and Expense Overview'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Amount ($)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Days of the Week'
                        }
                    }
                }
            }
        });
    } else {
        console.error("Weekly chart data is not defined.");
    }
});
document.addEventListener('DOMContentLoaded', () => {
    // Get the canvas element for the weekly chart
    const ctx = document.getElementById('overallChart').getContext('2d');

    // Check if weeklyChartData is available
    if (typeof weeklyChartData !== 'undefined') {
        const { labels, overall} = weeklyChartData;

        // Create the bar chart
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels, // Days of the week
                datasets: [
                    {
                        label: 'Overall',
                        data: overall,
                        backgroundColor: '#1B9C85',
                        borderColor:  '#1B9C85',
                        borderWidth: 2
                    },
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false, // Allow the chart to adjust size responsively
                plugins: {
                    title: {
                        display: true,
                      
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Amount ($)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Days of the Week'
                        }
                    }
                }
            }
        });
    } else {
        console.error("Weekly chart data is not defined.");
    }
});

document.addEventListener("DOMContentLoaded", function () {
    if (!Array.isArray(expenseLabels) || !Array.isArray(expenseValues) || expenseLabels.length === 0) {
        console.error("Expense data is missing or not formatted correctly.");
        return;
    }

    if (!Array.isArray(incomeLabels) || !Array.isArray(incomeValues) || incomeLabels.length === 0) {
        console.error("Income data is missing or not formatted correctly.");
        return;
    }

    // Expense Pie Chart
    var expenseCtx = document.getElementById("expensePieChart").getContext("2d");
    new Chart(expenseCtx, {
        type: "pie",
        data: {
            labels: expenseLabels,
            datasets: [{
                data: expenseValues,
                backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4CAF50", "#9C27B0"],
                hoverOffset: 5
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { 
                    position: "bottom",
                    labels:{
                        font: {
                            size: 20,
                            weight: 'bold'
                        },
                        padding: 20,
                    } }
            }
        }
    });

    // Income Pie Chart
    var incomeCtx = document.getElementById("incomePieChart").getContext("2d");
    new Chart(incomeCtx, {
        type: "pie",
        data: {
            labels: incomeLabels,
            datasets: [{
                data: incomeValues,
                backgroundColor: ["#3F51B5", "#009688", "#FF5722", "#795548", "#FFC107"],
                hoverOffset: 5
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { 
                    position: "bottom",
                    labels: {
                        font: {
                             size: 20,
                             weight: 'bold',
                        },
                        padding: 20,
                    }
                }
                
            }
        }
    });
});
