const chart = document.getElementById("careerChart");

if (chart) {

    new Chart(chart, {

        type: "bar",

        data: {

            labels: [
                "Technology",
                "Medical",
                "Business",
                "Government",
                "Creative"
            ],

            datasets: [{

                label: "Interest",

                data: [
                    12,
                    5,
                    8,
                    4,
                    6
                ]

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    display: true

                }

            }

        }

    });

}