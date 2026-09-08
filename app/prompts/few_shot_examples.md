1. [Funcional] Perfil de PO com permissões de Ordem de Serviço
   Descrição: Como administrador do sistema, eu quero criar um cargo de PO com
   permissões específicas para gerenciar Ordens de Serviço, para que o time
   possa corrigir apontamentos de arquivos no SharePoint sem depender de
   acesso administrativo total.
   Critérios de aceitação:
   - Dado que o administrador acessa o módulo de Cargos e Permissões,
     Quando ele cria um novo cargo do tipo "PO",
     Então o sistema deve permitir associar permissões de leitura e escrita
     sobre Ordens de Serviço e sobre a correção de apontamentos de arquivos
     no SharePoint, sem liberar outras áreas administrativas.
   Story Points / Priority: 3 · Alta

2. [Funcional] Escolha de formato e destino na geração de documentos
   Descrição: Como usuário do módulo de Ordem de Serviço, eu quero escolher o
   formato (PDF ou DocX), o destino (SharePoint e/ou download) e a pasta de
   salvamento antes de gerar o documento, para que o arquivo final já saia
   organizado da forma que preciso.
   Critérios de aceitação:
   - Dado que o usuário está na tela de geração de documentos,
     Quando ele seleciona o formato desejado e o destino (SharePoint,
     download, ou ambos),
     Então o sistema deve gerar o arquivo no formato escolhido e salvá-lo
     no(s) destino(s) selecionado(s).
   - Dado que o usuário optar por usar a pasta da competência do mês,
     Quando ele confirmar a geração,
     Então o sistema deve localizar ou criar automaticamente essa pasta antes
     de salvar o arquivo.
   Story Points / Priority: 5 · Alta

3. [Técnica] Criação automática da estrutura de pastas no SharePoint
   Descrição: Como sistema de geração de documentos, eu quero criar
   automaticamente a hierarquia de pastas (termo aditivo → mês → OS →
   subpastas de entrega) quando ela não existir no SharePoint, para que
   nenhuma geração de documento falhe por ausência de estrutura.
   Critérios de aceitação:
   - Dado que o caminho de destino no SharePoint (ex.: Ordem de Serviço >
     Termo Aditivo > pasta do mês > pasta da OS) não existe,
     Quando o sistema tenta salvar um documento gerado,
     Então ele deve criar toda a hierarquia de pastas faltante, incluindo as
     subpastas padrão de entrega (ex.: TAP, RAT), antes de salvar o arquivo.
   - Dado que já exista mais de uma OS no mesmo mês para o mesmo cliente,
     Quando um novo documento dessa OS for gerado,
     Então o sistema deve direcionar o arquivo para a pasta da OS
     correspondente, sem duplicar a estrutura de pastas do mês.
   Story Points / Priority: 5 · Média

4. [Melhoria] Liberação de geração de documentos por projeto
   Descrição: Como administrador, eu quero liberar a geração de documentos
   por projeto (ex.: SES-MS, SES-PE) de forma independente, para que cada
   projeto opere com sua própria estrutura de termo aditivo sem impactar os
   demais.
   Critérios de aceitação:
   - Dado que um novo projeto precisa ser liberado para geração de
     documentos,
     Quando o administrador configurar o ambiente correspondente (produção,
     não teste),
     Então o sistema deve gerar documentos seguindo a estrutura de pastas
     específica daquele projeto (ex.: primeiro ou segundo termo aditivo),
     sem afetar os demais projetos configurados.
   Story Points / Priority: 2 · Média

5. [Funcional, em elaboração] Geração do racional a partir do catálogo de serviços
   Descrição: Como usuário do módulo de Ordem de Serviço, eu quero montar o
   racional da OS a partir do catálogo de serviços do cliente, para que eu
   não precise construir esse racional manualmente fora do sistema.
   Critérios de aceitação:
   - Dado que o cliente possui um catálogo de serviços cadastrado
     (referência: catálogo do SES-MS),
     Quando o usuário seleciona os serviços aplicáveis à OS dentro do
     módulo,
     Então o sistema deve montar automaticamente o racional com base nos
     itens selecionados do catálogo, permitindo edição manual antes de
     salvar.
   Story Points / Priority: 8 (estimativa preliminar) · A definir
