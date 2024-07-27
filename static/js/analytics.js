 
 // Fetch data from JSON file
 const BACKEND_URL = `https://dashboard.missingpersonsug.org/api/victim-statistics`
 fetch(BACKEND_URL)
     .then(response => {
         if (!response.ok) {
             throw new Error('Network response was not ok');
         }
         return response.json();
     })
     .then(records => {
         const lastKnownLocation = new Counter();

         // Iterate through the records and update counters
         const {data} = records;

         // Create charts with the data
         createChart('genderChart', 'pie', data.gender, 'Gender Distribution');
         createChart('statusChart', 'pie', data.status, 'Status Distribution');
         createChart('holdingLocationChart', 'pie', data.holding_locations, 'Holding Location Distribution');
         createChart('lastKnownLocationChart', 'pie', data.last_known_location, 'Holding Location Distribution');
     })
     .catch(error => console.error('Error fetching JSON data:', error));

 // Helper class for counting occurrences
 class Counter {
     constructor() {
         this.counts = {};
     }

     increment(key) {
         if (this.counts[key]) {
             this.counts[key]++;
         } else {
             this.counts[key] = 1;
         }
     }
 }

 function createChart(elementId, chartType, data, label) {
     const ctx = document.getElementById(elementId).getContext('2d');

      // Define color schemes for different charts
    const colorSchemes = {
        genderChart: [
            "rgba(54, 162, 235, 1)",
            "rgba(255, 99, 132, 1)",
            "rgba(255, 206, 86, 1)",
        ],
        statusChart: [
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
            "rgba(199, 199, 199, 1)",
        ],
        holdingLocationChart: [
        "rgba(255, 69, 58, 1)", // Bright red
        "rgba(10, 132, 255, 1)",   // Vivid blue
        "rgba(255, 214, 10, 1)",   // Bright yellow
        "rgba(48, 209, 88, 1)",    // Lime green
        "rgba(191, 90, 242, 1)",   // Vibrant purple
        "rgba(255, 159, 10, 1)",   // Bright orange
        "rgba(0, 199, 190, 1)",    // Teal
        "rgba(255, 55, 95, 1)",    // Hot pink
        "rgba(64, 200, 224, 1)",   // Sky blue
        "rgba(100, 210, 80, 1)",   // Green
        ],
        lastKnownLocationChart: [
            "rgba(255, 159, 64, 1)",
            "rgba(199, 199, 199, 1)",
            "rgba(83, 102, 255, 1)",
            "rgba(40, 159, 64, 1)",
            "rgba(210, 199, 199, 1)",
        ],
    };

    // Choose the appropriate color scheme based on the elementId
    const backgroundColor = colorSchemes[elementId] || [
       "rgba(255, 69, 58, 1)", // Bright red
        "rgba(10, 132, 255, 1)",   // Vivid blue
        "rgba(255, 214, 10, 1)",   // Bright yellow
        "rgba(48, 209, 88, 1)",    // Lime green
        "rgba(191, 90, 242, 1)",   // Vibrant purple
        "rgba(255, 159, 10, 1)",   // Bright orange
        "rgba(0, 199, 190, 1)",    // Teal
        "rgba(255, 55, 95, 1)",    // Hot pink
        "rgba(64, 200, 224, 1)",   // Sky blue
        "rgba(100, 210, 80, 1)",   // Green
    ];

     new Chart(ctx, {
         type: chartType,
         data: {
             labels: Object.keys(data),
             datasets: [{
                 label: label,
                 data: Object.values(data),
                 borderWidth: 1,
                backgroundColor: backgroundColor,
                borderColor: backgroundColor.map(color => color.replace("0.8", "1")),
             }]
         },
         options: {
             scales: {
                 y: {
                     beginAtZero: true
                 }
             }
         }
     });
 }
