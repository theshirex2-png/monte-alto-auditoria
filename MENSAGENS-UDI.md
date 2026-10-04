# Monte Alto — lista verificada do nicho UDI

Nicho: **empreendimentos onde uma falha de segurança custa capital.**
Incorporadoras, construtoras e administradoras de condomínio.

Por que este nicho e não outro: quem tem VGV de centenas de milhões e
administradora de 25 anos tem orçamento e tem dor. Pet shop não paga
R$ 550.

**Tudo abaixo foi medido hoje, não inferido.** Antes de reenviar qualquer
mensagem, reconfirme: site muda.

---

## Achado comum a quatro dos seis

`/wp-json/wp/v2/users` responde **HTTP 200** e devolve o slug do
administrador. Quem cuida do site pode ser descoberto em uma requisição, sem
força bruta. Isso corta pela metade o trabalho de quem tenta entrar.

| alvo | users | id 1 | expõe |
|---|---|---|---|
| AC Administradora | 200 | `admin` | **login `admin`** |
| Morar Construtora | 200 | `morar` | 4 usuários: morar, andre, mktmorar |
| Condominius | 200 | `swarmtecnologia` | login da empresa de tecnologia |
| Condonal | 200 | `condonal` | + hostname websiteseguro.com |
| Grand Construtora | 401 | — | bloqueado, correto |
| CEMA Vet | 401 | — | bloqueado, correto |

Leitura honesta: Grand e CEMA fazem o certo. Isso é argumento a favor de
ti — mostra que tu sabe a diferença entre exposto e bloqueado, e não está
acusando todo mundo do mesmo.

---

## 1. Morar Construtora — o melhor da lista

- https://www.morar.com.br
- WhatsApp: (27) 3314-1500
- 12 mil unidades entregues, 77 empreendimentos, R$ 1,2 bi em VGV.

**Medido:** `/wp-json/` com 18 namespaces. `/wp-json/wp/v2/posts` devolve
**477 posts**. `/wp-json/wp/v2/users` com **HTTP 200** — expõe os usuários
`morar` (id 1), `andre` (id 10) e `mktmorar` (id 11). Login bloqueado em
`/wp-login.php`, o que é correto, mas não compensa a API.

Plugins: Contact Form 7, Instagram Feed, **WP Rocket** (cache pago).
Pagou plugin pago. Tem orçamento.

**Mensagem:**

Oi, tudo bem? Auditei o site da Morar e achei uma exposição concreta: em
`/wp-json/wp/v2/users` o WordPress devolve o nome de usuário do
administrador — hoje responde com `morar`, `andre` e `mktmorar`, incluindo
o id 1. É uma requisição só, sem tentar senha. A tela de login em
`/wp-login.php` está bloqueada, o que é correto e mostra que alguém já pensou
nisso, mas a API entrega o que o login esconde.

Em construtora com 477 posts publicados e ativo em toda a região, isso é o tipo de
detalhe que um concorrente de tabela ou um golpe de engenharia social usa
para chegar no time de marketing. Não é vazamento de dado de cliente.

Faço a varredura completa e te entrego o que mais importa: o que está
exposto além disso, plugins com correção pendente e o que está rodando
atrás. Sem custo e sem compromisso — se fizer sentido, a gente fala de
corrigir. Posso rodar?

---

## 2. AC Administração de Condomínios — 35 anos

- https://acadm.com.br
- (27) 99762-1717 · maurilio@acadm.com.br
- Administradora em Vila Velha e Vitória, 35 anos de operação.

**Medido:** WordPress 7.0.5. `/wp-json/wp/v2/users` com HTTP 200 expõe
**`admin` (id 1)** e `acadm` (id 3). `/wp-login.php` responde 200 — a tela
de login está no lugar. 14 namespaces na API.
Plugins: Contact Form 7, Cookie Law Info, Amin Chat Button, Page Links To.

**Mensagem:**

Oi. Vi o site da AC Administração e tenho um achado específico: o
endpoint `/wp-json/wp/v2/users` do WordPress está devolvendo os logins do
painel. Hoje responde com o usuário `admin` — que é o primeiro conta criada
em qualquer instalação de WordPress, justamente o primeiro nome que scanner
tenta. A tela de login em `/wp-login.php` está funcionando, então o site
está no ar normalmente; o problema é que a API entrega o que ela deveria
esconder.

Administradora com 35 anos e condôminos que pagam taxa todo mês tem nome e
documento na mão. Falha aqui não é só o site cair, é dado de condômino.
Faço a varredura completa, te entrego tudo com arquivo e linha, sem custo.
Posso rodar?

---

## 3. Condominius — administradora Grande Vitória

- https://condominius-es.com.br
- condominius@condominius-es.com.br

**Medido:** WordPress 7.1.2, LiteSpeed. `/wp-json/` com **16 namespaces**.
`/wp-json/wp/v2/users` HTTP 200 expõe `swarmtecnologia` (id 1) — login da
empresa de tecnologia que mantém o site. 33 posts.
Plugins: Elementor Pro, JetEngine, form-masks-for-elementor,
country-code-field-for-elementor, Cookie Law Info, Pixelyoursite Pro.
São seis plugins de formulário e marketing sobre o mesmo formulário.

**Mensagem:**

Oi. Auditei o site da Condonal e o achado é de servidor, não de conteúdo: o
endpoint `/wp-json/wp/v2/users` devolve a conta de administrador com id 1, e
o campo de endereço dela aponta para `condonal1.websiteseguro.com`. Isso
revela que a administração do site roda em servidor de terceiro, separado
do site que está no ar.

Duas coisas somam aí: o hostname da administração fica público, e quem
controla esse servidor de terceiro tem o painel. Em administradora com 25
de anos e presença no ranking do ES, uma falha aqui não é o site ficar
lento.

Faço a varredura completa — mapeio a cadeia entre o site e o painel, e o que
exige ação. Sem custo. Posso rodar?

---

## 5. Grand Construtora — alto padrão, ponta de Itaparica

- https://www.grandconstrutora.com.br
- WhatsApp: (27) 3329-1515 · (27) 99846-0015

**Medido:** WordPress 7.1.2, LiteSpeed. `/wp-json/` com 12 namespaces, 91
posts. `/wp-json/wp/v2/users` devolve **HTTP 401** — bloqueado, correto.
`/wp-login.php` responde 200. Plugins: Contact Form 7, Easy FancyBox.

**Por que entra mesmo assim:** a API exposta com 12 namespaces e
`/wp-login.php` no lugar não é falha grave, mas é superfície. E construtora
de alto padrão com lançamento ativo tem injetação de lead por formulário
como ativo comercial — vale saber o que o formulário aceita.

**Mensagem:**

Oi. O site da Grand Construtora está com a enumeração de usuário
bloqueada — `/wp-json/wp/v2/users` devolve 401. É a configuração certa, e
digo isso porque a maioria dos sites que eu audito está aberto. Boa parte do
trabalho já está feita aí.

O que ainda está exposto é a superfície: `/wp-json/` responde com 12
namespaces e `/wp-login.php` está acessível. Em construtora de alto padrão
com lançamento ativo, o formulário não é só contato — é o canal por onde
entra o lead. Quero saber o que ele aceita e o que devolve.

Faço a varredura e te entrego o mapa, com o que é risco real separado do
que é só superfície. Sem custo. Posso rodar?

---

## 6. CEMA Veterinária — Serra

- https://cemaes.com.br
- (27) 3068-4455 · (27) 99775-4455 (WhatsApp)

**Medido:** WordPress 7.1.2. `/wp-json/` com 8 namespaces,
`/wp-json/wp/v2/posts` devolve 6 posts, `/wp-login.php` responde 200.
Enumeração de usuário bloqueada (401). Plugin: Contact Form 7.

Entra como referência de volume, não de valor. Clínica 24h, telefone no
título — bom sinal de que site é canal de venda real.

**Mensagem:**

Oi. Vi o site da CEMA e o que está em aberto: a API REST responde em
`/wp-json/` com 8 namespaces e `/wp-json/wp/v2/posts` devolve o conteúdo do
site inteiro, sem autenticação. `/wp-login.php` está acessível, e tem
Contact Form 7 instalado.

A enumeração de usuário está bloqueada, o que é correto. O que sobra é a
superfície do formulário, que em clínica 24h é onde entra phishing de
"seu pet foi vacinado, pague a segunda dose".

Faço a varredura completa e te entrego o que importa primeiro. Sem custo.
Posso rodar?

---

## Como enviar

Morar e Grand e CEMA são WhatsApp. AC aceita WhatsApp ou e-mail.
Condominius e Condonal, e-mail.

Uma vez. Sem resposta em 24h, uma segunda. Depois para.

Se pedirem referência, menciona 43 testes de regressão no teu script e que
o laudo sai em PDF com arquivo e linha. Não inventa cliente anterior.