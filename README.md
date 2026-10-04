# Monte Alto Auditoria

Auditoria de codigo para **incorporadoras, construtoras e administradoras de
condominio** no Espirito Santo.

Uma falha de seguranca em site de empresa desse porte nao custa lentidao.
Custa lead, custa e-mail falseado com o nome da marca, custa dado de
condomino. E por isso que o alvo da auditoria nao e o site bonito: e o
dinheiro que para quando o site falha.

---

## O problema que este servico resolve

Varredura automatica em plugin WordPress real devolve **546 pontos**. Mandar
546 linhas para o cliente nao e auditoria, e ruido: esconde o sinal e diz ao
decisor que quem vendeu nao sabe o que fez.

O servico e a **triagem**. Agrupar por arquivo e padrao, separar o que e
falha do autor do que e dependencia de terceiro, e entregar o que exige
acao com arquivo, linha e correcao sugerida.

### Resultado medido — WP File Manager 8.0.6

Plugin real, baixado do repositorio oficial do WordPress. 295 arquivos PHP.

| | |
|---|---|
| Pontos brutos da varredura | **546** |
| Grupos por arquivo e padrao | **42** |
| Grupos acionaveis | **28** |
| Severidade alta ou critica | **9** |

Um dos 9 graves, lido no codigo fonte:

```
wp-file-manager/lib/php/elFinderSession.php:206

$data = unserialize(base64_decode($var));
```

`unserialize()` reconstroi objetos PHP. Se a sessao for manipulavel, o
atacante escolhe qual classe instanciar — e dispara o construtor dela.
`base64_decode` nao e protecao: e codificacao.

---

## Como a triagem funciona

| Criterio | O que faz |
|---|---|
| **Por arquivo e padrao** | 514 escritas de arquivo viram um item. O que importa e o padrao do autor, nao a linha. |
| **Codigo de terceiro e dependencia** | Achado em jQuery, CodeMirror ou elFinder nao e falha de quem usa o plugin. Vira "atualizar dependencia". |
| **Nada e escondido** | Todo achado continua no laudo. A triagem muda a ordem de leitura, nao o que existe. |
| **Diz o que esta certo** | Se a enumeração de usuario esta bloqueada, o laudo diz. Distinguir exposto de bloqueado e o trabalho. |

---

## Precos

| Servico | Valor | O que entrega |
|---|---|---|
| **Varredura completa** | R$ 550 | Site ou plugin mapeado, achado com arquivo e linha, agrupado por padrao, laudo em PDF, correcao sugerida |
| **Auditoria completa** | R$ 2.400 | Tudo da varredura, analise de fluxo de dado em cada critico, prioridade de ataque encadeada, reuniao de 60 min, 5 dias uteis |
| **Correcao** | R$ 180/hora | So depois do diagnostico. Orcado antes de comecar. |

Prestador **pessoa fisica**: Luiz Claudio Oliveira dos Santos. PIX direto, sem
nota fiscal. Se o processo do cliente exigir documento fiscal, isso e
negociado a parte e pode alterar o valor.

---

## Limite do que e feita

E leitura de codigo. Nao e teste de invasao, nao e pentest, nao e
exploracao. Nenhum acesso e tentado e nenhuma credencial e testada. O
relatorio se obtem por autorizacao do titular do site, por escrito.

Um achado estatico indica onde o codigo permite o ataque, nao que o ataque
ocorreu. Por isso o laudo vem com a explicacao do porque a linha e um risco,
e nao apenas com o que mudar.

---

## Metodo

A varredura roda sobre a copia do codigo que o cliente envia — um `.zip` ou
acesso a repositorio. Nada e instalado no servidor do cliente, nenhum
acesso e exigido, nenhum plugin e ativado.

O script tem suite de regresao propria: **43 casos de teste** que cobrem
Python, PHP e WordPress, incluindo casos que **nao devem** gerar achado —
SQL com prepared statement, senha com bcrypt, `htmlspecialchars` antes do
echo. Falso positivo em laudo pago custa a confianca do cliente — por isso a
suite de teste cobre tambem os casos que NAO devem gerar achado.

Cobertura medida:

- 23 casos de bateria propria (14 positivos, 9 negativos): **0 falso
  negativo, 0 falso positivo**
- 43 casos de regressao: **43/43**

---

## Contato

**Luiz Claudio Oliveira dos Santos** — Monte Alto Auditoria
Serra e Vila Velha, ES · atendimento em todo o estado

- WhatsApp: 27 99818-5280
- E-mail: luizoliveiraa839@gmail.com

---

## Site

<https://theshirex2-png.github.io/monte-alto-auditoria/>

O codigo deste repositorio e a landing page do servico.
