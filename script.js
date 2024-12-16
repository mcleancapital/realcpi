// Data for the charts (replace with API data or fetch from a file)
const sp500Data = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
  datasets: [{
    label: 'S&P 500',
    data: [3750, 3850, 3950, 4050, 4000, 4100, 4200, 4250, 4300, 4400, 4500, 4600],
    borderColor: 'rgba(75, 192, 192, 1)',
    borderWidth: 2,
    fill: false,
  }]
};

const peRatioData = {
  labels: ['2020', '2021', '2022', '2023', '2024'],
  datasets: [{
    label: 'PE Ratio',
    data: [20, 25, 23, 24, 22],
    borderColor: 'rgba(255, 99, 132, 1)',
    borderWidth: 2,
    fill: false,
  }]
};

// Chart.js Configuration
const ctx1 = document.getElementById('sp500Chart').getContext('2d');
new Chart(ctx1, {
  type: 'line',
  data: sp500Data,
  options: {
    responsive: true,
    plugins: {
      legend: { display: true },
    },
  },
});

const ctx2 = document.getElementById('peRatioChart').getContext('2d');
new Chart(ctx2, {
  type: 'line',
  data: peRatioData,
  options: {
    responsive: true,
    plugins: {
      legend: { display: true },
    },
  },
});
