const dadosMock = {
    "AC": { desemprego: "8.2%", inflacao: "4.5%", periodo: "2024-04" },
    "AL": { desemprego: "9.0%", inflacao: "4.3%", periodo: "2024-04" },
    "AP": { desemprego: "7.5%", inflacao: "3.9%", periodo: "2024-04" },
    "AM": { desemprego: "6.8%", inflacao: "4.2%", periodo: "2024-04" },
    "BA": { desemprego: "10.1%", inflacao: "4.6%", periodo: "2024-04" },
    "CE": { desemprego: "...", inflacao: "...", periodo: "..." },
    "DF": { desemprego: "...", inflacao: "...", periodo: "..." },
    "ES": { desemprego: "...", inflacao: "...", periodo: "..." },
    "GO": { desemprego: "...", inflacao: "...", periodo: "..." },
    "MA": { desemprego: "...", inflacao: "...", periodo: "..." },
    "MT": { desemprego: "...", inflacao: "...", periodo: "..." },
    "MS": { desemprego: "...", inflacao: "...", periodo: "..." },
    "MG": { desemprego: "...", inflacao: "...", periodo: "..." },
    "PA": { desemprego: "...", inflacao: "...", periodo: "..." }, 
    "PB": { desemprego: "...", inflacao: "...", periodo: "..." },
    "PR": { desemprego: "...", inflacao: "...", periodo: "..." },
    "PE": { desemprego: "...", inflacao: "...", periodo: "..." },
    "PI": { desemprego: "...", inflacao: "...", periodo: "..." },
    "RJ": { desemprego: "...", inflacao: "...", periodo: "..." },
    "RN": { desemprego: "...", inflacao: "...", periodo: "..." },
    "RS": { desemprego: "...", inflacao: "...", periodo: "..." },
    "RO": { desemprego: "...", inflacao: "...", periodo: "..." },
    "RR": { desemprego: "...", inflacao: "...", periodo: "..." },
    "SC": { desemprego: "...", inflacao: "...", periodo: "..." },
    "SP": { desemprego: "...", inflacao: "...", periodo: "..." },
    "SE": { desemprego: "...", inflacao: "...", periodo: "..." },
    "TO": { desemprego: "...", inflacao: "...", periodo: "..." }
  };

  const estados = document.querySelectorAll("svg path");
const infoDiv = document.getElementById("info");
const mapa = document.getElementById("mapa");

estados.forEach((estado) => {
  estado.addEventListener("click", (event) => {
    event.stopPropagation();

    estados.forEach(e => e.classList.remove("selecionado"));
    estado.classList.add("selecionado");

    const uf = estado.id;
    const info = dadosMock[uf];

    if (info) {
      infoDiv.innerHTML = `
        <h2>${uf}</h2>
        <p><strong>Taxa de Desemprego:</strong> ${info.desemprego}</p>
        <p><strong>Inflação:</strong> ${info.inflacao}</p>
        <p><strong>Período:</strong> ${info.periodo}</p>
      `;
    } else {
      infoDiv.innerHTML = `<p>Dados não disponíveis para ${uf}.</p>`;
    }
  });
});

document.addEventListener("click", (event) => {
  if (!mapa.contains(event.target)) {
    estados.forEach(e => e.classList.remove("selecionado"));
    infoDiv.innerHTML = `
      <h2>Informações</h2>
      <p>Selecione um estado para ver os dados.</p>
    `;
  }
});