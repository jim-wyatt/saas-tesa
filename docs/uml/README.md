# UML Diagrams (PlantUML)

This folder contains typical UML diagrams for the SaaS TESA project.

## Diagrams

- [Component Diagram source](component-diagram.puml) | [SVG](images/component-diagram.svg) | [PNG](images/component-diagram.png)
- [Domain Class Diagram source](domain-class-diagram.puml) | [SVG](images/domain-class-diagram.svg) | [PNG](images/domain-class-diagram.png)
- [Ingestion Sequence Diagram source](ingestion-sequence-diagram.puml) | [SVG](images/ingestion-sequence-diagram.svg) | [PNG](images/ingestion-sequence-diagram.png)
- [Deployment Diagram source](deployment-diagram.puml) | [SVG](images/deployment-diagram.svg) | [PNG](images/deployment-diagram.png)

## Previews

### Component Diagram

![Component Diagram PNG](images/component-diagram.png)

![Component Diagram](images/component-diagram.svg)

### Domain Class Diagram

![Domain Class Diagram PNG](images/domain-class-diagram.png)

![Domain Class Diagram](images/domain-class-diagram.svg)

### Ingestion Sequence Diagram

![Ingestion Sequence Diagram PNG](images/ingestion-sequence-diagram.png)

![Ingestion Sequence Diagram](images/ingestion-sequence-diagram.svg)

### Deployment Diagram

![Deployment Diagram PNG](images/deployment-diagram.png)

![Deployment Diagram](images/deployment-diagram.svg)

## Render options

- VS Code: install a PlantUML extension and open any `.puml` file.
- CLI with Docker:

  ```bash
  docker run --rm -v "$PWD":/work -w /work plantuml/plantuml docs/uml/*.puml
  ```

- Local Java install:

  ```bash
  plantuml docs/uml/*.puml
  ```
