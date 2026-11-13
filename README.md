# NEXO — Laboratório de Cybersecurity

**Criado por Gabriel Henrik.**

**Autoria e titularidade do código próprio: Gabriel Henrik Menezes Alves.**

Copyright © 2026 Gabriel Henrik Menezes Alves. Código próprio sob licença proprietária; consulte LICENSE, AUTHORS.md e THIRD_PARTY_NOTICES.md. Esta licença não é uma licença de software livre. A documentação e a interface identificam limitações reais e não prometem invulnerabilidade ou certificação pericial.

## O que é

NEXO é uma plataforma de proteção e investigação digital com ambientes por perfil. O fluxo é **login real → escolha do perfil → criação/desbloqueio do cofre → guia introdutório → uso das ferramentas**. A seleção de perfil adapta a interface e não comprova cargo ou concede autorização sobre sistemas externos.

| Perfil | Experiência |
|---|---|
| Pessoa comum / pessoa física | Proteção de contas, geração local de senhas, inspeção de links e arquivos |
| Pessoa jurídica / empresa | Organização de ativos, riscos e casos; sem colaboração multiusuário implementada |
| PF / investigação institucional | Casos, fontes, evidências, mapa e linha do tempo; sem terminal ou ferramentas de pentest |
| Hacking / cibersegurança | OSINT, análise de arquivos, catálogo de integrações e testes em escopo autorizado |

O perfil PF é autodeclarado. O produto não representa afiliação ou aprovação da Polícia Federal.

## Funcionalidades reais

- DNS público (Google Public DNS), RDAP de domínios e rede/ASN IPv4 (RIPEstat), com fonte, horário e limitações.
- SHA-256 de arquivos de até 25 MB no navegador; conteúdo não enviado ao servidor. Não é análise antivírus.
- Inspeção local da estrutura de URLs e geração criptográfica de senhas; não é cofre de credenciais.
- Casos, evidências, locais documentados, linha do tempo e relatórios. Coordenadas são informadas a partir de fontes; não há rastreamento de pessoas.
- OpenStreetMap, carregado mediante ação explícita; o provedor recebe IP e regiões de tiles consultadas.
- Cofre cifrado no cliente: AES-256-GCM, PBKDF2-SHA-256 (600.000 iterações), salt e IV aleatórios, chave não extraível mantida em memória. A frase não é enviada ao servidor. Sem a frase, não há recuperação.
- Backups criptografados, importação local e relatórios em texto aberto mediante confirmação.
- Guias introdutórios próprios para os quatro perfis, com quatro etapas e perguntas de verificação. O progresso fica no cofre. A conclusão remove o guia da tela inicial; ele pode ser reaberto pelo menu. Não é uma certificação profissional.
- Integrações declarativas instaláveis no cofre, com catálogo, importação validada, execução e registro de resultados em casos. Veja docs/INTEGRACOES.md.

## O que ainda depende de infraestrutura

- **IA:** há uma integração server-side com OpenAI Responses. Precisa de OPENAI_API_KEY no ambiente. Não há modelo próprio treinado. Perguntas e contexto compartilhado com IA ficam fora da proteção ponta a ponta do cofre; o contexto é opt-in com confirmação.
- **Linux e Nmap:** o adaptador em runner/ usa parâmetros fixos, identidade e redes explicitamente configuradas no servidor. Precisa ser instalado em um Linux isolado com HTTPS. Não foi validado em um container em execução ou contra um alvo real; testes unitários cobrem validação e parsing. O site não executa Kali, shell arbitrário ou captura de pacotes.
- **Outras ferramentas:** Wireshark, TShark, Sherlock e ferramentas adicionais não estão integrados. Cada nova ferramenta exige um adaptador, isolamento, revisão de licença, testes e publicação. O catálogo não deve ser confundido com instalação irrestrita de ferramentas.
- O globo global é uma simulação visual rotulada; não há telemetria de ataques ao vivo.

## Como começar como usuário

1. Abra /login e entre com a conta autorizada na plataforma. O site mantém a política privada do proprietário.
2. Escolha pessoa comum, empresa, investigação institucional/PF ou cibersegurança.
3. Crie uma frase secreta longa e exclusiva e guarde-a em um gerenciador. Registros antigos só são migrados para cifra quando você cria o cofre e conclui o salvamento. Cópias e backups antigos não são apagados por essa migração.
4. Complete o guia do seu perfil. Você pode consultar as áreas do app pelo menu durante o aprendizado.
5. Abra um caso. Registre o objetivo, fontes e limitações. Faça uma consulta ou análise, revise o resultado e salve como evidência.
6. Para integrações, use o perfil cibersegurança → Integrações → Instalar ou Importar JSON → Executar → Salvar no caso. Apenas adaptadores disponíveis são aceitos.
7. Exporte backups cifrados periodicamente. Relatórios em texto ficam fora do cofre. Bloqueie o cofre ou saia ao terminar.

## Arquitetura e arquivos

- web/ — interface, criptografia, módulos declarativos, cursos e Leaflet local.
- server/api.mjs — APIs autenticadas, fontes públicas, armazenamento de envelopes cifrados e pontes opcionais de IA/Linux.
- server/security.mjs — CSP, HSTS, no-store, no-referrer e demais cabeçalhos.
- scripts/build.mjs — compilação determinística que embute os assets no Worker ESM.
- dist/server/index.js — Worker compilado, com export default.fetch.
- runner/ — adaptador opcional Linux, Dockerfile, compose e instruções.
- tests/ — validação, autorização, criptografia, fluxos de UI e runner.
- docs/ e examples/ — documentação e exemplo de manifesto.

## Compilar e testar

Requisitos: Node.js >= 22.16 com import.meta.dirname, Python 3 para testes do runner. Não há dependências npm para instalar; Leaflet já está incluído com sua licença.

```sh
npm run build
npm test
```

O artefato não é um site estático para abrir via file://. Ele depende de um runtime compatível com Workers, identidade confiável da plataforma Sites e um binding R2 chamado BUCKET. Em outra hospedagem, identidade, armazenamento, TLS e permissões devem ser implementados explicitamente; não confie em cabeçalhos de identidade enviados diretamente pelo visitante.

## Publicar

A configuração da instância atual está em .openai/hosting.json. A publicação Sites usa o commit exato e um arquivo contendo .openai/hosting.json e dist/server/index.js. Este ZIP inclui o código e a compilação, mas não contém credenciais de hospedagem, dados de usuários ou chaves do cofre.

O acesso privado e a autenticação são geridos pela plataforma Sites. Em hospedagem própria, nunca publique a API aceitando livremente oai-authenticated-user-id como prova de identidade; esse header só é confiável atrás do gateway que autentica e substitui o valor.

## Segredos opcionais

Configure no servidor, nunca em arquivos versionados, browser ou chat:

- OPENAI_API_KEY; OPENAI_MODEL opcional, padrão gpt-4.1-mini.
- LINUX_RUNNER_URL: origem HTTPS do executor isolado.
- LINUX_RUNNER_TOKEN: segredo de serviço compartilhado com o executor.
- No executor: NEXO_RUNNER_TOKEN, NEXO_ALLOWED_CIDRS e NEXO_ALLOWED_HOSTS.

Veja SECURITY.md e runner/README.md. A frase do cofre jamais deve ser usada como segredo de API ou token de serviço.

## Limites de segurança e autoria

A criptografia protege o conteúdo do cofre no armazenamento. Consultas a fontes, IA, mapas externos e relatórios em texto têm limites próprios, explicados na interface. A segurança depende também do dispositivo, navegador e código entregue pelo servidor. Não foi feita uma auditoria independente nem uma revisão visual em navegador neste ambiente. Os testes automatizados não substituem essas avaliações.

A licença reserva direitos sobre o código próprio, mas não impede tecnicamente cópias. Licenças e autorias de terceiros permanecem intactas. O projeto contou com assistência de ferramentas de IA.

Repositório indicado pelo criador: https://github.com/gabrielhenrik0704-dot/NEXO---Laborat-rio-de-Cybersecurity
