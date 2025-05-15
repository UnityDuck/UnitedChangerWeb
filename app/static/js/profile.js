function toggleUpload() {
    const form = document.getElementById('uploadForm');
    form.style.display = (form.style.display === 'none' || form.style.display === '') ? 'block' : 'none';
}

const apiKey = 'eGCvr06hXSw0oinclXKs';

async function fetchAndRenderChart() {
  const from = document.getElementById('currencyFrom').value;
  const to = document.getElementById('currencyTo').value;
  const currencyPair = `${from}${to}`;

  const endDate = new Date().toISOString().split('T')[0];
  const start = new Date();
  start.setMonth(start.getMonth() - 3);
  const startDate = start.toISOString().split('T')[0];

  const url = `https://marketdata.tradermade.com/api/v1/timeseries?currency=${currencyPair}&api_key=${apiKey}&start_date=${startDate}&end_date=${endDate}&format=records`;

  try {
    const response = await fetch(url);
    const data = await response.json();
    const records = data.quotes;

    if (!records || records.length === 0) {
      alert("Нет данных для выбранной валютной пары.");
      return;
    }

    const trace = {
      x: records.map(r => r.date),
      open: records.map(r => r.open),
      high: records.map(r => r.high),
      low: records.map(r => r.low),
      close: records.map(r => r.close),
      type: 'candlestick',
      increasing: { line: { color: '#26a69a' } },
      decreasing: { line: { color: '#ef5350' } }
    };

    const layout = {
      dragmode: 'zoom',
      margin: { r: 10, t: 25, b: 40, l: 60 },
      paper_bgcolor: '#0d1117',
      plot_bgcolor: '#0d1117',
      font: { color: '#e0e0e0' },
      xaxis: {
        title: 'Дата',
        type: 'category',
        showgrid: false,
        tickangle: -45,
        tickfont: {
          size: 9,
          color: '#c0c0c0'
        },
        tickvals: []
      },
      yaxis: {
        showgrid: true,
        gridcolor: '#2c2c3e'
      }
    };
    document.getElementById('chartTitle').textContent = `График ${from} / ${to}`;

    Plotly.newPlot('candlestick-chart', [trace], layout, { responsive: true });

  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
    alert('Произошла ошибка при получении данных.');
  }
}

document.getElementById('currencyFrom').addEventListener('change', fetchAndRenderChart);
document.getElementById('currencyTo').addEventListener('change', fetchAndRenderChart);

fetchAndRenderChart();

const flagMap = {
RUB: "ru",
USD: "us",
CNY: "cn",
PLN: "pl",
RSD: "rs",
CAD: "ca",
GBP: "gb",
EUR: "eu",
CHF: "ch",
JPY: "jp",
KZT: "kz",
AED: "ae"
};

function updateFlag(selectId, imgId) {
    const select = document.getElementById(selectId);
    const img = document.getElementById(imgId);
    select.addEventListener('change', () => {
      const code = select.value;
      const flagCode = flagMap[code];
      img.src = `https://flagcdn.com/w40/${flagCode}.png`;
    });
}

updateFlag("currencyFrom", "flagFrom");
updateFlag("currencyTo", "flagTo");

document.getElementById("converter-form").addEventListener("submit", async function(e) {
e.preventDefault();

const from = document.getElementById("from_currency").value.toUpperCase();
const to = document.getElementById("to_currency").value.toUpperCase();
const amount = parseFloat(document.getElementById("amount").value);

if (from === to) {
    showResult("Выберите разные валюты для конвертации.");
    return;
}

document.getElementById('spinner').classList.remove('d-none');
document.getElementById('result-box').classList.add('d-none');

try {
    const response = await fetch(`https://api.coinbase.com/v2/exchange-rates?currency=${from}`);
    const data = await response.json();

    const rate = data.data.rates[to];
    if (!rate) {
      showResult("Курс для выбранных валют пока не поддерживается.");
      return;
    }

    const result = amount * parseFloat(rate);
    showResult(`${amount.toFixed(2)} ${from} = ${result.toFixed(2)} ${to}`);
    } catch (error) {
      console.error("Ошибка при получении курса:", error);
      showResult("Произошла ошибка при получении курса обмена.");
    } finally {
      document.getElementById('spinner').classList.add('d-none');
      document.getElementById('result-box').classList.remove('d-none');
    }
});

function showResult(message) {
    const box = document.getElementById("result-box");
    box.textContent = message;
    box.classList.remove("d-none");
}

const supportedCurrencies = [
  "RUB", "USD", "CNY", "PLN", "RSD", "CAD",
  "GBP", "EUR", "CHF", "JPY", "KZT", "AED"
];

let ratesMatrix = {};

async function fetchRates(base) {
  const res = await fetch(`https://api.coinbase.com/v2/exchange-rates?currency=${base}`);
  const data = await res.json();
  return data.data.rates;
}

async function updateRatesMatrix() {
  for (let base of supportedCurrencies) {
    try {
      const rates = await fetchRates(base);
      ratesMatrix[base] = {};
      for (let target of supportedCurrencies) {
        if (base === target) {
          ratesMatrix[base][target] = "1.0000";
        } else {
          ratesMatrix[base][target] = parseFloat(rates[target]).toFixed(4) || "—";
        }
      }
    } catch (e) {
      console.error(`Ошибка при получении курса ${base}:`, e);
      if (!ratesMatrix[base]) {
        ratesMatrix[base] = {};
        for (let target of supportedCurrencies) {
          ratesMatrix[base][target] = base === target ? "1.0000" : "—";
        }
      }
    }
  }
}

function renderTable() {
  const oldWrapper = document.getElementById("ratesTableWrapper");
  if (oldWrapper) oldWrapper.remove();

  const footer = document.querySelector("footer");

  const table = document.createElement("table");
  table.className = "table table-bordered table-dark table-sm table-striped border-secondary mb-5";

  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");
  headerRow.appendChild(Object.assign(document.createElement("th"), { textContent: "From / To" }));

  for (let cur of supportedCurrencies) {
    const th = document.createElement("th");
    th.textContent = cur;
    headerRow.appendChild(th);
  }
  thead.appendChild(headerRow);
  table.appendChild(thead);

  const tbody = document.createElement("tbody");
  for (let base of supportedCurrencies) {
    const row = document.createElement("tr");
    const baseCell = document.createElement("th");
    baseCell.textContent = base;
    row.appendChild(baseCell);

    for (let target of supportedCurrencies) {
      const cell = document.createElement("td");
      cell.textContent = ratesMatrix[base]?.[target] || "—";
      row.appendChild(cell);
    }
    tbody.appendChild(row);
  }
  table.appendChild(tbody);

  const wrapper = document.createElement("div");
  wrapper.id = "ratesTableWrapper";
  wrapper.className = "container my-5";
  wrapper.appendChild(table);

  footer.parentNode.insertBefore(wrapper, footer);
}

function getFilenameFromInput() {
  const input = document.getElementById("graphFileName");
  let filename = input?.value.trim();
  if (!filename) filename = "rates_matrix.csv";
  if (!filename.endsWith(".csv")) filename += ".csv";
  return filename;
}

function downloadCSV(content, filename) {
  const blob = new Blob([content], { type: "text/csv;charset=utf-8;" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  link.style.display = "none";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

function saveGraph() {
  if (!ratesMatrix || Object.keys(ratesMatrix).length === 0) {
    alert("Таблица ещё не загружена, подождите...");
    return;
  }

  let csv = "From\\To," + supportedCurrencies.join(",") + "\n";

  for (let base of supportedCurrencies) {
    let row = [base];
    for (let target of supportedCurrencies) {
      row.push(ratesMatrix[base]?.[target] || "");
    }
    csv += row.join(",") + "\n";
  }

  const filename = getFilenameFromInput();
  downloadCSV(csv, filename);
}

async function init() {
  await updateRatesMatrix();
  renderTable();

  setInterval(async () => {
    await updateRatesMatrix();
    renderTable();
  }, 10_000);
}

init();
