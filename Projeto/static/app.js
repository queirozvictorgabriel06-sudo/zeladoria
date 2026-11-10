const API = ""; // vazio = a tela é servida pela própria API (mesmo endereço)
const GN = {1: "Baixo", 2: "Médio", 3: "Grave"};
const VIEWS = ["painel", "ocorrencias", "categorias", "consultas"];
const S = {b: [], p: [], c: [], o: [], view: "painel", erro: null, ok: false, f: {q: "", b: "", g: "", s: "1"}};
const $ = s => document.querySelector(s);
const esc = t => String(t).replace(/[&<>"']/g, c => "&#" + c.charCodeAt(0) + ";");
const shape = g => `<span class="g g${g}"><i></i>${GN[g]}</span>`;
const count = (arr, k) => { const m = {}; arr.forEach(x => m[x[k]] = (m[x[k]] || 0) + 1); return m; };
const uso = c => S.o.filter(o => o.problema === c.problema && o.gravidade === c.gravidade).length;
const optP = () => S.p.map(p => `<option value="${p.id_problema}">${esc(p.problema)}</option>`).join("");

function toast(t, err) {
  const d = document.createElement("div");
  d.className = "toast" + (err ? " err" : "");
  d.textContent = t;
  $("#toasts").append(d);
  setTimeout(() => d.remove(), 4500);
}

async function api(path, opt = {}) {
  // Render e Neon "dormem" quando ficam parados: avisa se a resposta demorar
  const slow = setTimeout(() => { $("#msg").hidden = false; $("#msg").textContent = "Acordando o servidor… na primeira visita isso pode levar cerca de um minuto."; }, 4000);
  try {
    const r = await fetch(API + path, {...opt, headers: {"Content-Type": "application/json"}});
    const d = await r.json().catch(() => null);
    if (!r.ok) { const m = d && d.detail; throw new Error(Array.isArray(m) ? m.map(x => x.msg).join(" ") : m || "Erro " + r.status); }
    return d;
  } finally { clearTimeout(slow); $("#msg").hidden = true; }
}

async function load() {
  const st = $("#st"); st.className = "pill"; st.textContent = "Conectando…";
  try {
    const r = {};
    // uma chamada por vez de propósito: a API usa um único cursor no banco
    for (const [k, u] of [["b", "/bairros"], ["p", "/problemas"], ["c", "/categorias/"], ["o", "/ocorrencias/"]]) {
      r[k] = await api(u);
      if (!Array.isArray(r[k])) throw new Error("A API respondeu, mas não conseguiu ler o banco. Se ela ficou parada por um tempo, reinicie o serviço no Render.");
    }
    Object.assign(S, r, {erro: null, ok: true});
    st.className = "pill ok"; st.textContent = "API online";
    
    // Correção: verifica se o elemento #upd existe antes de atualizar o texto
    const upd = $("#upd");
    if (upd) {
      upd.textContent = "Atualizado às " + new Date().toLocaleTimeString("pt-BR", {hour: "2-digit", minute: "2-digit"}) + ".";
    }
  } catch (e) {
    console.error("Erro no load:", e);
    // Correção: filtra apenas erros reais de fetch/rede
    const eRede = e instanceof TypeError && (e.message.includes("fetch") || e.message.includes("NetworkError"));
    S.erro = eRede ? "Não consegui falar com a API. Confira se ela está no ar e tente de novo." : e.message;
    st.className = "pill off"; st.textContent = "API offline";
  }
  render();
}

function painel() {
  const at = S.o.filter(o => o.ativo), n = at.length;
  const gc = [1, 2, 3].map(g => at.filter(o => o.gravidade === g).length);
  const rank = (k, t) => {
    const e = Object.entries(count(at, k)).sort((a, b) => b[1] - a[1]).slice(0, 5), mx = e.length ? e[0][1] : 1;
    return `<section class="card"><h2>${t}</h2>` + (e.length
      ? e.map(([nome, q]) => `<div class="rk"><span>${esc(nome)}</span><b>${q}</b><div class="bar"><i style="width:${q / mx * 100}%"></i></div></div>`).join("")
      : `<p class="empty">Nenhuma ocorrência ativa.</p>`) + `</section>`;
  };
  return `<section class="hero"><p class="big">${n}</p><div><h1>ocorrências ativas</h1>
    <p class="mut">em ${Object.keys(count(at, "bairro")).length} bairros. ${S.o.length - n} já foram resolvidas.</p></div></section>
    <div class="road" role="img" aria-label="Ocorrências ativas por gravidade">${n ? gc.map((q, i) => q ? `<b style="width:${q / n * 100}%;background:var(--g${i + 1})"></b>` : "").join("") : ""}</div>
    <div class="legend">${[1, 2, 3].map(g => `<span>${shape(g)} <b>${gc[g - 1]}</b></span>`).join("")}</div>
    <div class="kpis">${[["var(--blue)", S.o.length, "Ocorrências registradas"], ["var(--g1)", (S.o.length ? Math.round((S.o.length - n) / S.o.length * 100) : 0) + "%", "Taxa de resolução"], ["var(--g3)", gc[2], "Graves ativas"], ["var(--mut)", S.c.length, "Categorias cadastradas"]].map(([c, v, t]) => `<div class="kpi" style="--c:${c}"><b>${v}</b><span>${t}</span></div>`).join("")}</div>
    <div class="cols">${rank("bairro", "Bairros com mais ocorrências")}${rank("problema", "Problemas mais frequentes")}${recentes()}</div>
    <a class="btn main" href="#ocorrencias">Ver ocorrências</a>`;
}

function ocorrencias() {
  const f = S.f;
  return `<div class="head"><h1>Ocorrências</h1><button class="btn main" data-act="nova">Nova ocorrência</button></div>
  <div class="filters">
    <input id="fq" type="search" placeholder="Buscar por problema ou bairro" aria-label="Buscar" value="${esc(f.q)}">
    <select id="fb" aria-label="Bairro"><option value="">Todos os bairros</option>${S.b.map(b => `<option${b.bairro === f.b ? " selected" : ""}>${esc(b.bairro)}</option>`).join("")}</select>
    <select id="fg" aria-label="Gravidade"><option value="">Qualquer gravidade</option>${[1, 2, 3].map(g => `<option value="${g}"${f.g == g ? " selected" : ""}>${GN[g]}</option>`).join("")}</select>
    <select id="fs" aria-label="Situação">${[["1", "Ativas"], ["0", "Resolvidas"], ["", "Todas"]].map(([v, t]) => `<option value="${v}"${f.s === v ? " selected" : ""}>${t}</option>`).join("")}</select>
  </div><div id="lista" class="card tw"></div>`;
}

function lista() {
  const f = S.f, q = f.q.toLowerCase();
  const r = S.o.filter(o => (!q || (o.problema + " " + o.bairro).toLowerCase().includes(q)) && (!f.b || o.bairro === f.b) && (!f.g || o.gravidade == f.g) && (f.s === "" || o.ativo === (f.s === "1"))).sort((a, b) => b.id - a.id);
  $("#lista").innerHTML = r.length
    ? `<table><thead><tr><th>Nº</th><th>Problema</th><th>Bairro</th><th>Gravidade</th><th>Situação</th><th><span class="sr">Ações</span></th></tr></thead><tbody>` +
      r.map(o => `<tr><td><span class="no">${o.id}</span></td><td>${esc(o.problema)}</td><td>${esc(o.bairro)}</td><td>${shape(o.gravidade)}</td><td><span class="st ${o.ativo ? "a" : "r"}">${o.ativo ? "Ativa" : "Resolvida"}</span></td><td><button class="btn del sm" data-act="del-o" data-id="${o.id}">Apagar</button></td></tr>`).join("") +
      `</tbody></table><p class="mut cnt">${r.length} de ${S.o.length} ocorrências</p>`
    : `<p class="empty">${S.o.length ? "Nenhuma ocorrência com esses filtros." : "Nenhuma ocorrência registrada. Use “Nova ocorrência” para criar a primeira."}</p>`;
}

function categorias() {
  return `<h1>Categorias</h1>
  <p class="mut">Uma categoria liga um problema a um nível de gravidade. É ela que define a gravidade ao registrar uma ocorrência.</p>
  <form id="fc" class="card form" style="margin-top:1rem">
    <label>Problema<select name="p" required><option value="">Escolha…</option>${optP()}</select></label>
    <fieldset class="seg"><legend>Gravidade</legend>${[1, 2, 3].map(g => `<label><input type="radio" name="g" value="${g}" required> ${shape(g)}</label>`).join("")}</fieldset>
    <div><button class="btn main">Cadastrar categoria</button></div>
  </form>
  <div class="card tw">` + (S.c.length
    ? `<table><thead><tr><th>Nº</th><th>Problema</th><th>Gravidade</th><th>Em uso</th><th><span class="sr">Ações</span></th></tr></thead><tbody>` +
      S.c.map(c => `<tr><td><span class="no">${c.id_categoria_problema}</span></td><td>${esc(c.problema)}</td><td>${shape(c.gravidade)}</td><td>${uso(c)} ocorrências</td><td><button class="btn del sm" data-act="del-c" data-id="${c.id_categoria_problema}">Apagar</button></td></tr>`).join("") + `</tbody></table>`
    : `<p class="empty">Nenhuma categoria ainda. Cadastre a primeira no formulário acima.</p>`) + `</div>`;
}

function consultas() {
  const co = count(S.o, "bairro"), cp = count(S.o, "problema");
  const col = (t, arr, k, m) => `<section class="card"><h2>${t}</h2>` + (arr.length
    ? `<table><tbody>${arr.map(x => `<tr><td>${esc(x[k])}</td><td class="mut">${m[x[k]] || 0} ocorrências</td></tr>`).join("")}</tbody></table>`
    : `<p class="empty">Nada cadastrado.</p>`) + `</section>`;
  return `<h1>Bairros e problemas</h1><p class="mut">Somente consulta: bairros e problemas são cadastrados direto no banco de dados.</p>
  <div class="cols" style="margin-top:1rem">${col("Bairros", S.b, "bairro", co)}${col("Problemas", S.p, "problema", cp)}</div>`;
}

const V = {painel, ocorrencias, categorias, consultas};

function render() {
  document.querySelectorAll("nav a").forEach(a => a.setAttribute("aria-current", a.dataset.v === S.view ? "page" : "false"));
  $("#app").innerHTML = S.erro
    ? `<section class="card"><h1>Sem acesso aos dados</h1><p>${esc(S.erro)}</p><button class="btn main" data-act="reload">Tentar de novo</button></section>`
    : !S.ok ? `<div class="sk"></div><div class="sk" style="margin-top:1rem"></div>` : V[S.view]();
  if (!S.erro && S.ok && S.view === "ocorrencias") lista();
  const h = $(".hero .big"); if (h) countUp(h, +h.textContent);
}

function route() { const h = location.hash.slice(1); S.view = VIEWS.includes(h) ? h : "painel"; $("#app").classList.add("anim"); render(); setTimeout(() => $("#app").classList.remove("anim"), 700); }

function confirmar(texto, fn) {
  const d = $("#dlg");
  d.innerHTML = `<form class="form"><h2>Apagar?</h2><p>${texto}</p><div class="row"><button type="button" class="btn sec" data-act="fechar">Cancelar</button><button class="btn del">Apagar</button></div></form>`;
  d.querySelector("form").onsubmit = async e => { e.preventDefault(); d.close(); await fn(); };
  d.showModal();
}

async function apagar(path, ok, dica) {
  try { await api(path, {method: "DELETE"}); toast(ok); await load(); }
  catch (e) { toast(dica && /encontrad/i.test(e.message) ? dica : e.message, true); }
}

function nova() {
  const d = $("#dlg");
  d.innerHTML = `<form id="fn" class="form"><h2>Nova ocorrência</h2>
    <label>Bairro<select name="b" required><option value="">Escolha…</option>${S.b.map(b => `<option value="${b.id}">${esc(b.bairro)}</option>`).join("")}</select></label>
    <label>Problema<select name="p" required><option value="">Escolha…</option>${optP()}</select></label>
    <fieldset class="seg" id="gr"><legend>Gravidade</legend><span class="mut">Escolha o problema primeiro.</span></fieldset>
    <div class="row"><button type="button" class="btn sec" data-act="fechar">Cancelar</button><button class="btn main">Registrar</button></div></form>`;
  d.showModal();
}

document.addEventListener("click", e => {
  const b = e.target.closest("[data-act]"); if (!b) return;
  const a = b.dataset.act, id = b.dataset.id;
  if (a === "fechar") $("#dlg").close();
  else if (a === "reload") load();
  else if (a === "nova") nova();
  else if (a === "del-o") confirmar(`A ocorrência <b>nº ${esc(id)}</b> será apagada definitivamente.`, () => apagar("/ocorrencias/" + id, "Ocorrência apagada."));
  else if (a === "del-c") {
    const c = S.c.find(x => x.id_categoria_problema == id), n = c ? uso(c) : 0;
    confirmar(`A categoria <b>nº ${esc(id)}</b> será apagada.` + (n ? ` Há ${n} ocorrências com este problema e esta gravidade; se alguma usar esta categoria, a API não vai deixar apagar.` : ""),
      () => apagar("/categorias/" + id, "Categoria apagada.", "Não foi possível apagar: a categoria não existe mais ou está sendo usada por alguma ocorrência."));
  }
});

document.addEventListener("input", e => {
  const m = {fq: "q", fb: "b", fg: "g", fs: "s"}[e.target.id];
  if (m) { S.f[m] = e.target.value; lista(); }
});

document.addEventListener("change", e => {
  if (e.target.name !== "p" || !e.target.form || e.target.form.id !== "fn") return;
  const nome = e.target.selectedIndex > 0 ? e.target.options[e.target.selectedIndex].text : "";
  const cs = S.c.filter(c => c.problema === nome).sort((a, b) => a.gravidade - b.gravidade);
  $("#gr").innerHTML = `<legend>Gravidade</legend>` + (!nome ? `<span class="mut">Escolha o problema primeiro.</span>`
    : cs.length ? cs.map(c => `<label><input type="radio" name="cat" value="${c.id_categoria_problema}" required> ${shape(c.gravidade)}</label>`).join("")
    : `<span class="mut">Este problema ainda não tem categoria. <a href="#categorias" data-act="fechar">Cadastre uma categoria</a> e volte aqui.</span>`);
});

document.addEventListener("submit", async e => {
  const f = e.target;
  if (f.id === "fc") {
    e.preventDefault();
    const nome = f.p.options[f.p.selectedIndex].text, g = +new FormData(f).get("g");
    if (S.c.some(c => c.problema === nome && c.gravidade === g)) return toast("Essa categoria já existe.", true);
    try { await api("/categorias/", {method: "POST", body: JSON.stringify({id_problema: +f.p.value, gravidade: g})}); toast("Categoria cadastrada."); await load(); }
    catch (x) { toast(x.message, true); }
  } else if (f.id === "fn") {
    e.preventDefault();
    const cat = new FormData(f).get("cat");
    if (!cat) return toast("Escolha um problema que tenha categoria cadastrada.", true);
    try {
      await api("/ocorrencias/", {method: "POST", body: JSON.stringify({id_categoria_p: +cat, id_bairros: +f.b.value})});
      $("#dlg").close(); toast("Ocorrência registrada."); location.hash = "#ocorrencias"; await load();
    } catch (x) { toast(x.message, true); }
  }
});

addEventListener("hashchange", () => { route(); scrollTo(0, 0); });
route();
load();

function countUp(el, n) {
  if (matchMedia("(prefers-reduced-motion:reduce)").matches) return;
  let t0;
  const passo = t => { t0 = t0 ?? t; const p = Math.min((t - t0) / 700, 1); el.textContent = Math.round(n * (1 - (1 - p) ** 3)); if (p < 1) requestAnimationFrame(passo); };
  requestAnimationFrame(passo);
}

function recentes() {
  return `<section class="card"><h2>Últimas ocorrências</h2>` + (S.o.length
    ? S.o.slice().sort((a, b) => b.id - a.id).slice(0, 5).map(o => `<div class="rk"><span><span class="no sm">${o.id}</span>${esc(o.problema)}, ${esc(o.bairro)}</span>${shape(o.gravidade)}</div>`).join("")
    : `<p class="empty">Nada registrado ainda.</p>`) + `</section>`;
}

// tema claro/escuro (lembra a escolha)
const raiz = document.documentElement;
try { if (localStorage.getItem("tema")) raiz.dataset.theme = localStorage.getItem("tema"); } catch (e) {}
$("#tm").onclick = () => {
  const escuro = raiz.dataset.theme ? raiz.dataset.theme === "dark" : matchMedia("(prefers-color-scheme:dark)").matches;
  raiz.dataset.theme = escuro ? "light" : "dark";
  try { localStorage.setItem("tema", raiz.dataset.theme); } catch (e) {}
};
