# Knowledge Graph: Model Extraction Attacks on GNNs

## Complete System Overview

This knowledge graph represents the complete Model Extraction Attacks on GNNs framework for bank fraud detection. The system combines data generation, GNN modeling, adversarial attacks, and visualization in a comprehensive security evaluation framework.

```mermaid
graph TD
    %% Data Generation
    A[Synthetic Generator] --> B[Data Loader]
    
    %% Model Components
    B --> C[Target GNN Model]
    C --> D[Attack Framework]
    
    %% Attack Execution
    D --> E[Surrogate Model]
    E --> F[Evaluation]
    
    %% Visualization
    C --> G[Target Visualization]
    E --> H[Extracted Visualization]
    
    %% Integration
    A --> I[Main Execution]
    B --> I
    C --> I
    D --> I
    G --> I
    H --> I
    
    %% Attack Scenarios
    D --> J[Attack Taxonomy]
    
    %% Data Flow
    style A fill:#e1f5fe
    style B fill:#e1f5fe
    style C fill:#f3e5f5
    style D fill:#ffebee
    style E fill:#e8f5e9
    style F fill:#fff3e0
    style G fill:#fce4ec
    style H fill:#fce4ec
    style I fill:#fff8e1
    style J fill:#e0f2f1
    
    class A,B data
    class C,D,E,F,G,H model
    class I, J execution
```

## Detailed Component Relationships

### Data Flow and Dependencies

```mermaid
graph LR
    %% Data Generation
    A[Synthetic Generator] --> B[CSV File]
    B --> C[Data Loader]
    
    %% Model Building
    C --> D[NetworkX Graph]
    C --> E[DGL Graph]
    E --> F[Target GNN Model]
    
    %% Attack Execution
    F --> G[Attack Framework]
    G --> H[Surrogate GNN Model]
    
    %% Evaluation
    H --> I[Evaluation]
    I --> J[Fidelity Measurement]
    
    %% Visualization
    F --> K[Target Visualization]
    H --> L[Extracted Visualization]
    
    %% Configuration
    M[Main Execution] --> B
    M --> G
    M --> J
    
    class A,C,D,E,F,G,H,I,J,K,L,M component
```

## System Architecture

### Core Components

```mermaid
graph TB
    %% Main Components
    A[Data Generation] --> B[Data Processing]
    B --> C[Model Training]
    C --> D[Attack Simulation]
    D --> E[Model Extraction]
    E --> F[Evaluation]
    F --> G[Visualization]
    
    %% Data Components  
    A --> H[CSV Data]
    B --> I[NetworkX Graph]
    B --> J[DGL Graph]
    C --> K[Target Model]
    D --> L[Adversary Knowledge]
    E --> M[Surrogate Model]
    F --> N[Fidelity Metric]
    G --> O[Visualizations]
    
    %% Interconnections
    K --> D
    M --> F
    I --> G
    J --> G
    M --> G
    
    style A fill:#e1f5fe,stroke:#000
    style B fill:#e1f5fe,stroke:#000
    style C fill:#f3e5f5,stroke:#000
    style D fill:#ffebee,stroke:#000
    style E fill:#e8f5e9,stroke:#000
    style F fill:#fff3e0,stroke:#000
    style G fill:#fce4ec,stroke:#000
    
    style H fill:#bbdefb,stroke:#000
    style I fill:#bbdefb,stroke:#000
    style J fill:#bbdefb,stroke:#000
    style K fill:#e1bee7,stroke:#000
    style L fill:#e1bee7,stroke:#000
    style M fill:#a5d6a7,stroke:#000
    style N fill:#ffcc80,stroke:#000
    style O fill:#f48fb1,stroke:#000
```

## Attack Framework Integration

### Detailed Attack Flow

```mermaid
graph LR
    %% Attack Setup
    A[Attack Type] --> B[Knowledge Level]
    B --> C[Adversary Graph]
    B --> D[Adversary Features]
    B --> E[Shadow Dataset]
    
    %% Attack Process
    F[Target Model] --> G[Query Nodes]
    G --> H[Get Responses]
    H --> I[Construct Surrogate]
    I --> J[Pre-train on Shadow]
    J --> K[Train on Queries]
    
    %% Evaluation
    K --> L[Evaluate Fidelity]
    L --> M[Results Analysis]
    
    %% Integration
    C --> I
    D --> I
    E --> J
    F --> H
    
    style A fill:#b39ddb,stroke:#000
    style B fill:#b39ddb,stroke:#000
    style C fill:#9575cd,stroke:#000
    style D fill:#9575cd,stroke:#000
    style E fill:#9575cd,stroke:#000
    style F fill:#8e24aa,stroke:#000
    style G fill:#8e24aa,stroke:#000
    style H fill:#8e24aa,stroke:#000
    style I fill:#4caf50,stroke:#000
    style J fill:#4caf50,stroke:#000
    style K fill:#4caf50,stroke:#000
    style L fill:#ff9800,stroke:#000
    style M fill:#ff9800,stroke:#000
```

## Component Interactions

### Data Flow Through System

```mermaid
sequenceDiagram
    participant S as Synthetic Generator
    participant D as Data Loader
    participant M as Model Training
    participant A as Attack Framework
    participant E as Evaluation
    participant V as Visualization
    
    S->>D: Generate CSV Data
    D->>M: Load DGL Graph
    D->>M: Load NetworkX Graph
    M->>A: Target Model Ready
    A->>A: Generate Adversary Knowledge
    A->>A: Construct Surrogate Model
    A->>E: Evaluate Fidelity
    M->>V: Target Visualization
    A->>V: Extracted Visualization
    E->>V: Report Results
```

## Knowledge Graph Summary

### Files Structure
```
notes/
├── project-overview.md
├── synthetic-generator.md
├── bank-data-loader.md
├── bank-gnn-model.md
├── bank-attacks.md
├── main-bank.md
├── bank-visualizer.md
└── attack-taxonomy.md
```

### Key Relationships
1. **Data Foundation**: Synthetic generator → Data loader → Model training
2. **Model Lifecycle**: Model training → Attack framework → Evaluation 
3. **Security Testing**: Attack framework → Surrogate model construction
4. **Results Visualization**: Model training + Attack framework → Visualizations
5. **System Integration**: Main execution coordinates all components

This comprehensive knowledge graph provides a complete understanding of the Model Extraction Attacks on GNNs framework, showing how all components interconnect and contribute to security evaluation of bank fraud detection systems.