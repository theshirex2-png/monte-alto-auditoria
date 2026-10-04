# AMOSTRA — WP File Manager 8.0.6 (gratuito, sem compromisso)

Plugin real, baixado do repositório oficial do WordPress.
**295 arquivos PHP · 546 pontos brutos → 28 grupos acionáveis.**

Esta é a demonstração. Não é a lista completa do teu site — é o que
aparece quando o site tem plugin com esta superfície.

---

## O que foi encontrado

| Grupo | Onde | Gravidade |
|---|---|---|
| include com variável | lib/php/autoload.php:39-45 | crítica |
| include com variável | lib/php/elFinderFlysystemGoogleDriveNetmount.php:630-969 | crítica |
| include com variável | lib/php/elFinderVolumeGoogleDrive.class.php:630-940 | crítica |
| include com variável | lib/php/elFinder.class.php:1512 | crítica |
| salto de PHP após `?>` | inc/backup.php:225 | crítica |
| SQL por concatenação | classes/db-backup.php:234-248 | alta |
| unserialize sem restringir classes | lib/php/elFinder.class.php:4840 | alta |
| unserialize sem restringir classes | lib/php/elFinderSession.php:206 | alta |
| execução de comando | lib/php/elFinder.class.php:5330-5331 | alta |

**Total: 9 grupos de 28 acionáveis.** Cada grupo traz arquivo, linha,
causa provável e correção sugerida.

---

## Os três mais graves, explicados

### 1. `include` com variável — Remote File Inclusion

`autoload.php:39-45` e os arquivos do Google Drive montam o caminho de
include a partir de uma variável:

```php
$file = ELFINDER_PHP_ROOT_PATH . '/' . $name . '.class.php';
return (is_file($file) && include_once($file));
```

O `is_file()` reduz o risco, mas não zera. Se qualquer outro ponto do
plugin permitir controlar `$name`, isso vira execução de arquivo
arbitrário no servidor.

**Correção sugerida:** validar `$name` contra uma allowlist de nomes de
classe antes de montar o caminho, com `realpath()` e comparação de
prefixo contra a raiz permitida.

### 2. `unserialize()` sem restringir classes — PHP Object Injection

`elFinder.class.php:4840` e `elFinderSession.php:206`:

```php
$data = unserialize(base64_decode($var));
```

`unserialize()` reconstrói objetos PHP. Se o dado de sessão for
manipulável, um atacante escolhe qual classe instanciar e dispara o
construtor — o que em muitas base de código vira execução de código.

`base64_decode` não é proteção: é codificação, não criptografia.

**Correção sugerida:** `unserialize($d, ['allowed_classes' => false])`
ou migrar para `json_decode()`.

### 3. SQL por concatenação — SQL Injection

`classes/db-backup.php:234-248` monta a consulta juntando variável dentro
da string:

```php
$wpdb->query("SELECT ... WHERE id = " . $id);
```

Quem controla `$id` controla a consulta. Em plugin de gerenciador de
arquivos, o `id` costuma vir de requisição.

**Correção sugerida:** `$wpdb->prepare($sql, $id)`.

---

## Sobre a nota

Nota de segurança calculada: **0/100** no WP File Manager 8.0.6, 546
pontos brutos. Elementor 3.5.5 dá 88 pontos e Contact Form 7 dá 69.

Isso **não** significa que o site está vulnerável a 546 ataques. Significa
que o plugin tem muita superfície e que ninguém revisou. É o tipo de
número que justifica uma auditoria com triage — que é o que está neste
documento: 28 grupos, com gravidade e linha.

---

## O que este laudo não é

Não é teste de invasão. Não é pentest. Nenhum sistema foi explorado,
nenhum acesso foi alterado. É leitura de código.

E o diagnóstico não é a correção: correção é orçada à parte.

---

**Monte Alto Auditoria** · 27 99818-5280
Luiz Claudio Oliveira dos Santos · pessoa física · Serra e Vila Velha, ES