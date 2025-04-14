const estados = document.querySelectorAll("svg path");

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
          <p><strong>Taxa de Desemprego:</strong> ${dados.desemprego ?? "Dados indisponíveis"}</p>
          <p><strong>Inflação:</strong> ${dados.inflacao ?? "Dados indisponíveis"}</p>
          <p><strong>Período:</strong> ${dados.periodo ?? "Dados indisponíveis"}</p>

        `;
      })
      .catch((err) => {
        infoDiv.innerHTML = `<p>Não foi possível carregar os dados para ${uf}.</p>`;
        console.error(err);
      });
  });
});

document.addEventListener("click", (event) => {
  const isPath = event.target.closest("svg path");
  if (!isPath) {
    estados.forEach((e) => e.classList.remove("selecionado"));
    const infoDiv = document.getElementById("info");
    infoDiv.innerHTML = `
      <h2>Selecione um estado</h2>
      <p>Clique em um estado do mapa para ver os dados de desemprego.</p>
    `;
  }
});
