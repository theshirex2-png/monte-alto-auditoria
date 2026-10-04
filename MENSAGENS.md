# Mensagens de primeiro contato — lista verificada

Cada mensagem cita **achado real, medido no site**. Nada genérico. Se tu
manda isso e o cliente olhar, ele vê que tu foi lá e viu.

Nunca diga que achou problema sem ter verificado. A tabela abaixo é o que
foi medido; se um dia tu reenviar, reveja antes.

---

## 1. CEMA Veterinária — Serra/ES

- Site: https://cemaes.com.br
- Contato: (27) 3068-4455 · (27) 99775-4455
- Por que é forte: clínica veterinária com atendimento 24h, e o telefone
  está no título da página — quem busca no Google já encontra.

**Medido neste site:**
- WordPress 7.1.2 com REST API respondendo em `/wp-json/`
- `/wp-json/wp/v2/posts` devolve o conteúdo do site, 6 posts
- `/wp-login.php` acessível
- Plugin Contact Form 7 instalado — porta de entrada de spam

**Mensagem:**

Oi, tudo bem? Vi o site da CEMA e notei que o WordPress está com a API
REST liberada — em `/wp-json/wp/v2/posts` qualquer pessoa consegue ler o
conteúdo do site inteiro, e a tela de login fica aberta em `/wp-login.php`.
Não é vazamento de dado de cliente, mas é o caminho que scanner
usa para descobrir plugin desatualizado.

Faço uma varredura técnica do site e te entrego os achados com arquivo e
linha. Sem custo e sem compromisso — se servir, a gente conversa sobre
corrigir. Posso rodar?

---

## 2. LeoWP — programador PHP/WordPress

- Site: https://leowp.com
- Contato: não há WhatsApp nem e-mail no site. Buscar em `leowp.com`
  página de contato ou LinkedIn.
- Por que é forte: WordPress 6.2.13, WooCommerce, e é programador.

**Medido neste site:**
- **WordPress 6.2.13** — versão de 2022. É o achado mais forte possível:
  versão defasada é porta de entrada conhecida.
- REST API exposta em `/wp-json/`
- `/wp-admin/` e `/wp-login.php` respondendo
- WooCommerce instalado
- Atrás do Cloudflare

**Mensagem:**

Oi, vi que o site está em WordPress 6.2.13. Essa é de 2022, e há correção
de segurança publicada depois — é o tipo de coisa que entrada de malware
aproveita. O site está atrás do Cloudflare, o que ajuda, mas a versão
antiga continua exposta em `/wp-content`.

Se tu quiser, faço a varredura e te entrego o que mais importa primeiro:
versões, plugins e o que está exposto. Sem custo.

---

## Como enviar

WhatsApp, quando tiver número. E-mail, quando tiver endereço. Sem número
e sem e-mail, não há canal — e essa é a razão pela qual o LeoWP fica
fora da lista de envio imediato.

Uma mensagem, uma vez. Sem resposta em 24h, uma segunda. Depois para.