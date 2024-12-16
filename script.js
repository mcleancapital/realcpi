// Example data for the first graph
const ctx1 = document.getElementById('graph1').getContext('2d');
new Chart(ctx1, {
  type: 'line',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [{
      label: 'S&P 500 P/E Ratio',
      data: [20.5, 21.2, 22.1, 23.0, 22.8],
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 2,
      fill: false,
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        display: true,
      },
    },
  },
});

// Example data for the second graph
const ctx2 = document.getElementById('graph2').getContext('2d');
new Chart(ctx2, {
  type: 'line',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [{
      label: 'Inflation Rate (%)',
      data: [3.2, 3.4, 3.1, 3.0, 2.9],
      borderColor: 'rgba(255, 99, 132, 1)',
      borderWidth: 2,
      fill: false,
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        display: true,
      },
    },
  },
});

// Example data for the third graph
const ctx3 = document.getElementById('graph3').getContext('2d');
new Chart(ctx3, {
  type: 'line',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [{
      label: 'Real CPI Index',
      data: [120, 122, 121, 123, 125],
      borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 2,
      fill: false,
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        display: true,
      },
    },
  },
});
