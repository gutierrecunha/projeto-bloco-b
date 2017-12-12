var dadosMapa;

function montaPopUp(linha) {
    htmlPopUp = "<ul>";
    htmlPopUp += "<li> Data -  " + linha.dataFormatada + "</li>";
    htmlPopUp += "<li> Ordem -  " + linha.ordem + "</li>";
    htmlPopUp += "<li> Velocidade -  " + linha.velocidade + " Km/h</li>";
    htmlPopUp += "</ul>";

    return htmlPopUp;
}

function montaMapa(data, linha, hora) {

    valorData = "";

    if (data) {
        valorData = "/" + data.replace("/", "-").replace("/", "-");
    }

    valorHora = "";

    if (hora) {
        valorHora = "/" + hora;
    }

    if (linha) {
        $("#btGraficos").show();
        $("#divLegenda").show();
        $("#divgraficos").css("left", "-45%");

        $.ajax({
            url: host + "/linha/" + linha + valorData + valorHora
        }).done(function(linhas) {
            dadosMapa = JSON.parse(linhas);
            montaMapaLinha(dadosMapa);
        });
    } else {
        $("#btGraficos").hide();
        $("#divLegenda").hide();
        $("#divgraficos").css("left", "-45%");
        markerGroup.clearLayers();
        mymap.setView([-22.9068, -43.1729], 10);
    }

}

function montaMapaLinha(arrayLinha) {
    markerGroup.clearLayers();
    //mymap.setView([arrayLinha[0].latitude, arrayLinha[0].longitude], 12);

    $("#velocidadeMaximaDia").text(" " + arrayLinha[0].velocidadeMaxima + " km/h");

    arrayLinha.forEach(function(linha) {


        cor = "yellow";

        if (linha.legendaVelocidade == "médio") {
            cor = "blue";
        } else if (linha.legendaVelocidade == "alto") {
            cor = "green";
        }

        var redMarker = L.VectorMarkers.icon({
            icon: 'bus',
            markerColor: cor
        });


        //L.polyline([[linha.latitude, linha.longitude]], { color: 'red' }).addTo(mymap);

        L.marker([linha.latitude, linha.longitude], { icon: redMarker }).bindPopup(montaPopUp(linha)).addTo(markerGroup);
        mymap.fitBounds(markerGroup.getBounds());
    });

    /*for (x = 0; x < arrayLinha.length; x++) {
        if (x < arrayLinha.length - 1) {
            L.polyline([
                [arrayLinha[x].latitude, arrayLinha[x].longitude],
                [arrayLinha[++x].latitude, arrayLinha[++x].longitude]
            ], { color: 'red' }).addTo(mymap);

            L.marker([arrayLinha[x].latitude, arrayLinha[x].longitude], ).bindPopup(montaPopUp(arrayLinha[x])).addTo(markerGroup);
        }
    }*/
}