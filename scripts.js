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
          <p><strong>Taxa de Desemprego:</strong> ${dados.desemprego}</p>
          <p><strong>Inflação:</strong> ${dados.inflacao}</p>
          <p><strong>Período:</strong> ${dados.periodo}</p>
        `;
      })
      .catch((err) => {
        infoDiv.innerHTML = `<p>Não foi possível carregar os dados para ${uf}.</p>`;
        console.error(err);
      });
  });
});
