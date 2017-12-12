function montaHora() {
    if ($("#comboLinhas").val() && $("#comboDatas").val()) {
        $.ajax({
            url: host + "/horas/" + $("#comboDatas").val().replace("/", "-").replace("/", "-") + "/" + $("#comboLinhas").val()
        }).done(function(horas) {

            $("#comboHoras").empty();
            $("#comboHoras").append("<option value=''>Selecione uma hora</option>");

            JSON.parse(horas).forEach(function(hora) {
                $("#comboHoras").append("<option value=" + hora.hora + ">" + hora.hora + "</option>");
            });
        });
    } else {
        $("#comboHoras").empty();
        $("#comboHoras").append("<option value=''>Selecione uma hora</option>");
    }
}



$(document).ready(function() {

    $.ajax({
        url: host + "/datas"
    }).done(function(linhas) {
        JSON.parse(linhas).forEach(function(data) {
            $("#comboDatas").append("<option value=" + data.data + ">" + data.data + "</option>");
        });
    });


    $.ajax({
        url: host + "/linhas"
    }).done(function(linhas) {
        JSON.parse(linhas).forEach(function(linha) {
            $("#comboLinhas").append("<option value=" + linha.linha + ">" + linha.linha + "</option>");
        });
    });

    $("#comboDatas").change(function() {
        montaMapa($("#comboDatas").val(), $("#comboLinhas").val());
        montaHora();
    });

    $("#comboLinhas").change(function() {
        montaMapa($("#comboDatas").val(), $("#comboLinhas").val());
        montaHora();
    });

    $("#comboHoras").change(function() {
        montaMapa($("#comboDatas").val(), $("#comboLinhas").val(), $("#comboHoras").val());
    });
});