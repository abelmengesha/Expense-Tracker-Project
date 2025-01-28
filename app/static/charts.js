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
                        borderWidth: 0.5
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

