function carregar_estados() {
    $.get({
      url: 'carregar_estados',
      data: {},
      success: (response) => {
        $("#estados").html(response);
        carregar_municipios();
      },
      fail: (response) => {},
    });
}


function carregar_municipios() {
    $.get({
      url: "carregar_municipios",
      data: {
        estado: $("#estados").val(),
      },
      success: (response) => {
        $("#municipios").html(response);
      },
      fail: (response) => {},
    });
  }


  function selecionar_estado(valor) {
    $.get({
      url: "selecionar_estado",
      data: {
        id: valor,
      },
      success: (response) => {
        $("#estados").html(response);
      },
      fail: (response) => {},
    });
  }

  function selecionar_municipio(valor) {
    $.get({
      url: "selecionar_municipio",
      data: {
        id: valor,
      },
      success: (response) => {
        $("#municipios").html(response);
      },
      fail: (response) => {},
    });
  }