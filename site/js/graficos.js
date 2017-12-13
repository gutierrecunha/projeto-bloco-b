Chart.defaults.global.elements.line.fill = false;

var c = document.getElementById("myChart");
var ctx = c.getContext("2d");
var myChart = new Chart(ctx, {});



$(document).ready(function() {

    $("#btGraficos").toggle();
    $("#divLegenda").toggle();

    $("#btGraficos").click(function() {
        $(this).toggle();
        $("#divgraficos").css("left", "1%");
    });

    $("#btGraficosVelocidade").click(function() {

        $.ajax({
            url: host + "/mediaVelocidadePorLinha/" + $("#comboLinhas").val()
        }).done(function(json) {

            json = JSON.parse(json);

            var arrayKeys = [];
            var arrayValues = [];
            Object.keys(json["velocidade"]).forEach(function(key) {
                arrayKeys.push(key);
                arrayValues.push(json["velocidade"][key]);
            });

            myChart.destroy();
            myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: arrayKeys,
                    datasets: [{
                        label: "Média de velocidade por Data - Linha " + $("#comboLinhas").val(),
                        backgroundColor: 'rgb(255, 99, 132)',
                        borderColor: 'rgb(255, 99, 132)',
                        data: arrayValues,
                    }, ]
                },
                options: {
                    tooltips: {
                        enabled: true,
                        callbacks: {
                            label: function(tooltipItems, data) {
                                return tooltipItems.yLabel + " km/h";
                            }
                        }
                    }
                }
            });

            $("#tituloModal").html("Média de Velocidade");
            $('#myModal').modal('show');
        });
















    });

    $("#btGraficosVelocidadeData").click(function() {

        data = $("#comboDatas").val().replace("/", "-").replace("/", "-");

        $.ajax({
            url: host + "/mediaVelocidadePorLinha/" + $("#comboLinhas").val() + "/" + data
        }).done(function(json) {

            json = JSON.parse(json);

            var arrayKeys = [];
            var arrayValues = [];
            //var arrayColors = [];

            Object.keys(json["velocidade"]).forEach(function(key) {
                arrayKeys.push(key);
                arrayValues.push(json["velocidade"][key]);

                //arrayColors.push('#' + Math.floor(Math.random() * 16777215).toString(16));
            });

            myChart.destroy();
            myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: arrayKeys,
                    datasets: [{
                        label: "Média de velocidade por Hora - Linha " + $("#comboLinhas").val(),
                        backgroundColor: '#00f',
                        borderColor: 'rgb(255, 99, 132)',
                        data: arrayValues,
                    }]
                },
                options: {
                    tooltips: {
                        enabled: true,
                        callbacks: {
                            label: function(tooltipItems, data) {
                                return tooltipItems.yLabel + " km/h";
                            }
                        }
                    }
                }
            });

            $("#tituloModal").html("Média de Velocidade por Hora");
            $('#myModal').modal('show');
        });




    });
});
