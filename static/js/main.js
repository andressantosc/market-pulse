
function revChart() {

    label_data = [];
    values_data = [];
    ticker = window.ticker;
    url = "http://localhost:5000/json/rev/";
    url = url.concat(ticker);

    $.getJSON(url, function(data){
        
        for (i=0; i < data.Data.data.length; i++) {
            label_data.push(data.Data.data[i].date);
            values_data[i] = data.Data.data[i].value;
        }
        var ctx = document.getElementById("myChart");
        var myChart = new Chart(ctx, {
            type: 'bar',
            multiTooltipTemplate: "<%=addCommas(value)%>",
            data: {
                labels: label_data,
                datasets: [{
                    label: 'USD',
                    data: values_data,
                    backgroundColor: 'rgba(0,100,0,0.5)',
                    borderWidth: 1,
                    borderColor: 'rgba(0,100,0,0.8)'
                }]
            },
            options: {
                tooltips: {
                  callbacks: {
                        label: function(tooltipItem, data) {
                            var value = data.datasets[0].data[tooltipItem.index];
                            value = value.toString();
                            value = value.split(/(?=(?:...)*$)/);
                            value = value.join(',');
                            return value;
                        }
                  } // end callbacks:
                }, //end tooltips
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero:false,
                            userCallback: function(value, index, values) {
                                // Convert the number to a string and splite the string every 3 charaters from the end
                                value = value.toString();
                                value = value.split(/(?=(?:...)*$)/);
                                value = value.join(',');
                                return value;
                            }
                        }
                    }]
                },
                title: {
                    display: true,
                    text: "Revenue",
                    fontSize: 16
                },
                legend: {
                    position: 'bottom'
                }
            }
        });
    });
}


function searchResults() {
    $("#myList").empty();
    name = document.getElementById("name").value;
    url = "http://localhost:5000/json/search/";
    url = url.concat(name);

    $.getJSON(url, function(data){
        $("#myList").append('<div id="results"><h2>Results:</h2>');

        for (i = 0; i < data.results.data.length; i++) {
            $("#myList").append('<h3 class="text-left sidepadding">Name: ' + data.results.data[i].name + "</h3>");
            $("#myList").append('<h4 class="text-left sidepadding">Ticker: ' + data.results.data[i].ticker + '<span class="text-right sidepadding text-green"><a href="http://localhost:5000/api/newcompany/' + data.results.data[i].ticker + '">Add to My Reports</a></span></h4>');
            $("#myList").append('<div class="hrule-full"></div>');
        }
    });
    document.getElementById("name").value = "";
    document.getElementById("name").blur();
}


