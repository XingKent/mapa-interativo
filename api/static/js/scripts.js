const estados = document.querySelectorAll("svg path");

//literalmente o q faz o mapa funcionar favor nao tocar nesta desgraça
estados.forEach((estado) => {
  estado.addEventListener("click", () => {
    estados.forEach((e) => e.classList.remove("selecionado"));
    estado.classList.add("selecionado");

    const uf = estado.id;
    const infoDiv = document.getElementById("info");

    fetch(`/api/indicadores/${uf}/`)
      .then((res) => {
        if (!res.ok) {
          throw new Error("Estado não encontrado");
        }
        return res.json();
      })
      .then((dados) => {
        infoDiv.innerHTML = `
          <h2>${dados.uf}</h2>
          <p><strong>Taxa de Desemprego: </strong> ${dados.desemprego ?? "Dados indisponíveis"}</p>
          <p><strong>Inflação: </strong> ${dados.inflacao ?? "Dados indisponíveis"}</p>
          <p><strong>Período: </strong> ${dados.periodo ?? "Dados indisponíveis"}</p>

        `;
      })
      .catch((err) => {
        infoDiv.innerHTML = `<p>Não foi possível carregar os dados para ${uf}.</p>`;
        console.error(err);
      });
  });
});


//click pra selecionar o estado
document.addEventListener("click", (event) => {
  const isPath = event.target.closest("svg path");
  if (!isPath) {
    estados.forEach((e) => e.classList.remove("selecionado"));
    const infoDiv = document.getElementById("info");
    infoDiv.innerHTML = `
      <h2>Selecione um estado</h2>
      <p>Clique em um estado do mapa para ver os dados.</p>
    `;
  }
});


//ocultar e mostrar as infos
document.addEventListener("DOMContentLoaded", function () {
  const toggleBtn = document.getElementById("toggleInfo");
  const infoText = document.getElementById("infoText");

  let infoVisible = false;

  toggleBtn.addEventListener("click", () => {
    infoVisible = !infoVisible;

    if (infoVisible) {
      infoText.classList.add("show-info");
      toggleBtn.innerHTML = '<img src="/static/img/close.png" class="close-img">';
      toggleBtn.title = "Clique para ocultar as informações";
    } else {
      infoText.classList.remove("show-info");
      toggleBtn.innerHTML = '<img src="/static/img/informacoes.png" class="info-img">';
      toggleBtn.title = "Clique para ver mais informações";
    }
  });
});