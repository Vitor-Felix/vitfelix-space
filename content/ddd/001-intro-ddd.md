---
title: DDD - Intro
---

## Definição Formal

> "Domain-Driven Design (DDD) é uma abordagem de desenvolvimento de software baseada na premissa de que o código deve ser estruturado em torno do domínio da aplicação e de sua lógica de negócio. Em sistemas complexos, o desenvolvimento deve ser focado no modelo do negócio, promovendo um alinhamento contínuo entre os especialistas do domínio (*Domain Experts*) e o time de engenharia por meio de um modelo conceitual compartilhado."  
> — *Eric Evans (2003)*

## Em outras palavras

DDD não é um framework, um padrão de pastas ou um tipo de banco de dados. É uma **filosofia de trabalho** para evitar que programadores construam sistemas que não resolvem a dor real do negócio. 

Em vez de começar o projeto decidindo a tabela do banco, você senta com quem entende da empresa e desenha o código com base nas regras do negócio real.

---

## Estratégico vs. Tático

* **Design Estratégico (Definição Técnica):** Conjunto de padrões organizacionais e modelagens de alto nível focados no mapeamento do domínio, na divisão de responsabilidades em subdomínios, no estabelecimento de fronteiras contextuais e no mapeamento de integração entre times e sistemas.  
  * *Em outras palavras:* O **mapa da cidade**. Define onde focar investimento, como dividir o sistema em áreas e como delimitar fronteiras.

* **Design Tático (Definição Técnica):** Padrões de projeto de software (*design patterns*) voltados à implementação do código de domínio purificado, garantindo o encapsulamento das regras de negócio e a integridade de invariants dentro de um modelo isolado de tecnologia.  
  * *Em outras palavras:* A **planta da casa**. Padrões de código usados para construir o software dentro dessas fronteiras.

---

## 1. Design Estratégico (Visão Macro)

### Subdomínios
**Definição:** Divisão lógica e operacional do problema de negócio em partes menores e mais gerenciáveis, categorizadas segundo o valor estratégico e a vantagem competitiva para a empresa.

* **Core (Principal):** A razão de existir da empresa e sua principal vantagem competitiva no mercado. Exige alto esforço de engenharia e código 100% customizado.
  * *Exemplo:* Algoritmo de recomendação da Netflix; sistema de otimização de rotas da DHL.
* **Suporte:** Aplicações necessárias para viabilizar as operações do Core Domain, porém sem gerar diferenciação no mercado. Geralmente possuem lógica simples (CRUDs).
  * *Exemplo:* Cadastro de filmes no catálogo da Netflix.
* **Genérico:** Processos operacionais padrão de mercado que não possuem regras exclusivas do negócio. Solucionados via softwares de terceiros (*SaaS*) ou bibliotecas prontas.
  * *Exemplo:* Módulo de faturamento/cobrança (integração via Gateway); serviço de autenticação de usuários.

### Bounded Contexts (Limites de Contexto)
**Definição:** Delimitação explícita de uma fronteira conceitual na qual um modelo de domínio específico se aplica com significado único, consistente e não ambíguo.

* *Exemplo:* Em um E-commerce:
  * No contexto de **Vendas**: `Produto` representa um item catalogado com preço, foto e promoções aplicáveis.
  * No contexto de **Estoque**: `Produto` representa um item físico armazenado com dimensões, peso e localização de prateleira.
  * No contexto de **Entrega**: `Produto` representa um volume a ser transportado vinculado a uma etiqueta e código de rastreio.

### Linguagem Ubíqua
**Definição:** Linguagem rigorosa e compartilhada, construída colaborativamente por desenvolvedores e *Domain Experts*, utilizada de forma idêntica nas conversas, documentações e na implementação do código fonte.

* *Exemplo:* Se a regra comercial é *"Cancelar Matrícula por Inadimplência"*, a implementação técnica refletirá o método `cancelarMatriculaPorInadimplencia()` (evitando jargões genéricos de programação como `updateStatus(0)` ou `setFlagActive(false)`).

---

## 2. Design Tático (Visão Micro / Código)

### Value Objects (Objetos de Valor)
**Definição:** Elementos imutáveis do modelo definidos exclusivamente por seus atributos (valores), sem identificação conceitual única.

* *Exemplo:* `CPF`, `Email`, `Dinheiro(valor, moeda)`. Se o valor for alterado, trata-se de uma nova instância distinta.

### Entities (Entidades)
**Definição:** Objetos de domínio que possuem uma identidade única e contínua ao longo de seu ciclo de vida, cujos atributos podem alterar de estado sem alterar a identidade do elemento.

* *Exemplo:* `Cliente(id: 123)`. Pode alterar nome, telefone e endereço, contudo permanece rastreável como o mesmo cliente no sistema.

### Aggregates (Agregados)
**Definição:** Grafo de Entidades e Objetos de Valor tratados como uma unidade coesa para modificação de dados, delimitados por uma raiz (*Aggregate Root*) responsável por garantir a consistência transactional e as invariants de negócio.

* *Exemplo:* A raiz `Pedido` gerencia o acesso às suas entidades filhas `ItemPedido`. O acesso direto a um item para alteração de valor é proibido; a modificação deve ser validada e executada pela raiz `Pedido`.

### Repositories (Repositórios)
**Definição:** Abstração da camada de persistência que simula uma coleção em memória de Agregados, isolando o modelo de domínio de detalhes técnicos de banco de dados ou frameworks.

* *Exemplo:* `pedidoRepository.salvar(pedido)`.

### Domain Events (Eventos de Domínio)
**Definição:** Notificação explícita de um evento de negócio relevante que ocorreu no passado dentro de um contexto delimitado, permitindo desacoplamento entre módulos.

* *Exemplo:* `PedidoPagoEvent`, `MatriculaCanceladaEvent`.

---

## DDD vs. Arquitetura Hexagonal: O quão similares?

**Não são a mesma coisa.** São abordagens complementares com propósitos distintos.

* **Podem ser usados separados?** Sim. É possível implementar a Arquitetura Hexagonal em projetos simples sem a modelagem tática/estratégica do DDD. Da mesma forma, é viável adotar o DDD utilizando outras arquiteturas (como *Clean Architecture* ou Arquitetura em Camadas).
* **Funcionam melhor juntos?** Sim, a sinergia é ideal. O DDD define *onde situar e como modelar as regras de negócio puras*, enquanto a Arquitetura Hexagonal (Ports & Adapters) fornece o *mecanismo arquitetural* para isolar o core do domínio de tecnologias externas (banco de dados, frameworks, adaptadores HTTP).

---

## Takeaway

Nem todo projeto precisa de DDD. Se o sistema é um CRUD simples (como o sistema da padaria da esquina), aplicar DDD gera complexidade desnecessária. DDD é a ferramenta ideal para sistemas complexos, onde a regra de negócio é densa e muda constantemente.