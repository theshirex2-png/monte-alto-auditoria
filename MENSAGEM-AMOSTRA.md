# Mensagem de primeiro contato — amostra de auditoria

---

## Versão WhatsApp (curta, para enviar agora)

Oi, tudo bem? Monte Alto Auditoria aqui.

Rodei uma varredura no WP File Manager 8.0.6, o gerenciador de arquivos
do WordPress, e encontrei alguns pontos graves no código do plugin. Não
entrou em nada, não explotei nada — só leitura de código.

O que apareceu, sem detalhar o quê:

- include com variável em 4 arquivos do plugin
- unserialize sem restringir classes em 2 pontos
- SQL montado por concatenação no módulo de backup

São 546 pontos brutos no total. Agrupados por arquivo e padrão, viram
28 grupos acionáveis, e 9 deles são graves.

Agrupar importa: 546 linhas de relatório ninguém lê. 9, sim.

Se quiser, te mando a amostra com arquivo, linha e a correção sugerida de
cada um. Sem custo e sem compromisso — se fizer sentido, a gente fala de
corrigir. Posso mandar?

---

## Versão e-mail (mais completa)

Assunto: WP File Manager 8.0.6 — 9 pontos graves em leitura de código

Prezado, bom dia.

Sou Luiz Claudio, da Monte Alto Auditoria. Rodamos análise estática no
código do plugin WP File Manager 8.0.6 e identificamos pontos que
merecem atenção antes que apareçam em auditoria de terceiro.

O que a varredura encontrou, agrupado:

| Grupo | Gravidade |
|---|---|
| include com variável — 4 arquivos do plugin | crítica |
| salto de PHP após `?>` em módulo de backup | crítica |
| SQL por concatenação no módulo de backup | alta |
| unserialize sem restringir classes — 2 pontos | alta |
| execução de comando no gerenciador | alta |

São 546 pontos brutos na varredura completa. Agrupados por arquivo e
padrão, restam 28 grupos acionáveis, sendo 9 de severidade alta ou
crítica. É esse agrupamento que manda a amostra: 546 linhas de relatório
não servem para nada, 9 servem.

Nada foi explorado. Nenhum acesso foi alterado. É leitura de código.

Se quiser, envio a amostra completa com arquivo, linha, causa provável e
correção sugerida. Sem custo e sem compromisso.

Atenciosamente,
Luiz Claudio Oliveira dos Santos
Monte Alto Auditoria · 27 99818-5280

---

## Por que esta mensagem funciona

**Diz o que encontrou, não o que é.** "include com variável" e
"SQL por concatenação" são nome de técnica. Quem decide sobre o site
entende e pergunta. Quem não entende, não decide e não perde teu tempo.

**Dá o número dos dois lados.** 546 brutos e 28 acionáveis. Isso mostra
que tu filtra, e filtrar é o serviço. Se dissesse só 546, pareceria
alarme. Se dissesse só 9, pareceria que não viu o resto.

**"Agrupados por arquivo e padrão"** — é o diferencial técnico. Fala
que existe processo, não só ferramenta.

**Não promete.** Diz que achou, diz que não explorou, diz que manda a
amostra se quiser. Quem manda amostra grátis e não cobra o envio já
demonstrou que sabe o que faz.

---

## Se responderem pedindo a amostra

Manda `AMOSTRA-WPFILEMANAGER.md` como PDF:

```
cd C:/Users/thesh/site-auditoria
python gerar-pdf.py <json> --saida AMOSTRA-WPFILEMANAGER.pdf
```

Depois, uma linha só, sem pressionar:

"Enviei. Se quiser, rodo o mesmo no restante do site e te passo o mapa
completo — R$ 550. Se não for o momento, sem problema."