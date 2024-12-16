document.addEventListener('DOMContentLoaded', () => {
  const ctx1 = document.getElementById('graph1').getContext('2d');
  const ctx2 = document.getElementById('graph2').getContext('2d');
  const ctx3 = document.getElementById('graph3').getContext('2d');

  new Chart(ctx1, {
    type: 'line',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
      datasets: [{
        label: 'Dataset 1',
        data: [20, 30, 40, 50, 60],
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 2,
        fill: false,
      }],
    },
    options: { responsive: true },
  });

  new Chart(ctx2, {
    type: 'line',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
      datasets: [{
        label: 'Dataset 2',
        data: [15, 25, 35, 45, 55],
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 2,
        fill: false,
      }],
    },
    options: { responsive: true },
  });

  new Chart(ctx3, {
    type: 'line',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
      datasets: [{
        label: 'Dataset 3',
        data: [10, 20, 30, 40, 50],
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 2,
        fill: false,
      }],
    },
    options: { responsive: true },
  });
});
