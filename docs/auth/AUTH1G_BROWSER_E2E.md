# Auth-1G — Browser E2E

## Objetivo

Validar autenticação, cookies, isolamento organizacional e revogação de
sessões usando Chromium, Playwright e PostgreSQL descartável no GitHub
Actions.

## Cenários

O Auth-1G cobre:

- login pela página `/login`;
- registro público permanentemente desabilitado;
- dois usuários provisionados diretamente no banco descartável;
- senhas armazenadas com Argon2id;
- dois tenants independentes;
- cookies reais de sessão;
- atributo `HttpOnly`;
- tokens diferentes entre usuários;
- acesso autorizado ao tenant próprio;
- resposta `404` para tenant externo;
- resposta `404` para usuário anônimo;
- segunda sessão do mesmo usuário;
- revogação das outras sessões;
- preservação da sessão atual;
- preservação da sessão de outro usuário;
- logout;
- regressões Auth-1B até Auth-1F;
- build do Next.js;
- pipeline Python.

## Ordem do banco

O Auth-1F é executado primeiro porque seu teste exige um banco vazio.

Depois das regressões, o script `web/scripts/auth1g-seed.ts` provisiona
as duas identidades e organizações usadas pelo navegador.

## Limites

O workflow não acessa:

- Railway;
- banco persistente;
- produção;
- Docker local;
- PostgreSQL local.

Nenhum cookie, token ou arquivo `storageState` é versionado.