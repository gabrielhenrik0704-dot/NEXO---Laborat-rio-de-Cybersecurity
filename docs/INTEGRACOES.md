# Instalar e integrar técnicas no NEXO

No perfil **Hacking / cibersegurança**, abra **Integrações**. Instale um fluxo do catálogo ou importe um manifesto JSON. A instalação salva a definição no seu cofre criptografado. Depois execute, revise as fontes e salve o resultado em um caso.

O formato é declarativo. Não contém JavaScript, comandos shell, binários, URLs de execução, credenciais ou endpoints livres. Importar um JSON não instala uma ferramenta Linux. Adaptadores novos exigem implementação no código, revisão das permissões/licença, testes e nova publicação. Isso preserva o limite de segurança do cofre e da hospedagem.

## Manifesto v1

Consulte examples/integracao-dominio.json. Troque o id para um identificador próprio, em letras minúsculas, números e hífens; informe nome, descrição e autor. A autoria declarada em um manifesto de terceiros não é verificada.

Campos: format=nexo-integration; version=1; id; name (até 90 caracteres); author (150); description (600); category=osint/investigation/pentest; inputType=domain/ip/url/file/host; steps (1 a 6).

| Adaptador | Entrada | Execução |
|---|---|---|
| dns | domain | Google Public DNS; recordType A/AAAA/MX/NS/TXT/CAA |
| rdap | domain | Registro público de domínio via RDAP |
| ripe | ip | IPv4 público, prefixo e ASN via RIPEstat |
| url_structure | url | Inspeção local, sem abrir o site |
| sha256 | file | Hash local, arquivo até 25 MB, sem upload |
| nmap_tcp | host | Trabalho no executor Linux configurado; etapa única; categoria pentest |

Todas as etapas de um fluxo usam a mesma entrada. Misturas incompatíveis são rejeitadas. Até 20 integrações por cofre. Campos desconhecidos e tipos não permitidos são rejeitados. Não existem instalação de scripts remotos ou execução de comandos arbitrários.

O resultado de Nmap fica pendente até o executor terminar. Use Atualizar trabalho; o app só permite salvar o fluxo como concluído quando recebe o resultado final. O executor e a autorização de rede continuam obrigatórios.

## Adicionar um adaptador novo ao código

1. Defina entradas e saídas, fontes, permissões, limites, proveniência e condições de licença.
2. Implemente o backend em server/api.mjs para fontes web fixas, ou um adaptador isolado específico no serviço Linux. Nunca aceite shell ou parâmetros livres.
3. Registre o identificador e o tipo de entrada em web/extensions.js, implemente a etapa correspondente em web/features.js e revise os limites de acesso no servidor.
4. Escreva testes de validação, falha, isolamento e resultados. Atualize THIRD_PARTY_NOTICES.md.
5. Compile e publique. Não anuncie o recurso como funcional antes de testar o serviço efetivo.

Fluxos que contêm dados de terceiros devem respeitar privacidade, autorização e os termos das fontes. Hash e coincidências de registro não comprovam autoria ou identidade.
