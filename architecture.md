
# System Architecture

## Overview
The LinkedIn Profile Extraction system is a modular Python application designed to scrape and parse LinkedIn profile data. It leverages **Playwright** for browser automation (handling login and page navigation) and a custom **Extractor Engine** for parsing HTML content into structured JSON.

## Key Components

### 1. Browser Automation (`loadState.py`)
- Manages the Playwright browser context.
- Handles user sessions and cookies.
- Navigates to profile URLs and dumps HTML content.

### 2. Extraction Engine (`extract_profile.py`)
- Reads HTML files from the disk.
- Orchestrates specific extractors for different profile sections.
- Produces normalized JSON output.

### 3. Extractor Modules (`extractors/`)
- **Registry**: Central repository of XPaths/Selectors.
- **BaseExtractor**: Abstraction for common extraction logic (fallback strategies, cleaning).
- **Specific Extractors**: Specialized classes for Headers, Metrics, Experience, Education, etc.

---

## Architecture Diagrams

### 1. System Context Diagram
This diagram illustrates the high-level data flow from the external LinkedIn website to the final JSON output.

```mermaid
graph TD
    %% Styling Definitions
    classDef person fill:#ff9900,stroke:#333,stroke-width:2px,color:white;
    classDef browser fill:#4285f4,stroke:#333,stroke-width:2px,color:white;
    classDef extractor fill:#34a853,stroke:#333,stroke-width:2px,color:white;
    classDef file fill:#fbbc05,stroke:#333,stroke-width:2px,color:black,stroke-dasharray: 5 5;
    classDef external fill:#ea4335,stroke:#333,stroke-width:2px,color:white;

    User((User)):::person -->|Configures| Config[config.toml]:::file
    User -->|Runs| Script[loadState.py / main.py]:::browser
    
    subgraph Browser Layer [Browser Layer]
        direction TB
        Script -->|Launches| Playwright[Playwright Browser]:::browser
        Playwright -->|Request| LinkedIn[LinkedIn.com]:::external
        LinkedIn -->|HTML Response| Playwright
        Playwright -->|Saves| HTMLFiles[HTML Files /profiles/]:::file
    end
    
    subgraph Extraction Layer [Extraction Layer]
        direction TB
        HTMLFiles -->|Reads| ExtractorEngine[extract_profile.py]:::extractor
        ExtractorEngine -->|Uses| Header[HeaderExtractor]:::extractor
        ExtractorEngine -->|Uses| Metrics[MetricsExtractor]:::extractor
        ExtractorEngine -->|Uses| Section[SectionExtractor]:::extractor
        
        Header -->|Lookups| Registry[Selector Registry]:::file
        Metrics -->|Lookups| Registry
        Section -->|Lookups| Registry
    end
    
    ExtractorEngine -->|Generates| JSON[profile.json]:::file
```

### 2. Class Diagram (Extractor Module)
This diagram details the object-oriented structure of the extraction logic.

```mermaid
classDiagram
    %% Styles
    style BaseExtractor fill:#f9f9f9,stroke:#333,stroke-width:2px,color:black
    style Registry fill:#fff3e0,stroke:#ff9800,stroke-width:2px,color:black
    style HeaderExtractor fill:#e8f5e9,stroke:#4caf50,stroke-width:2px,color:black
    style MetricsExtractor fill:#e8f5e9,stroke:#4caf50,stroke-width:2px,color:black
    style SectionExtractor fill:#e8f5e9,stroke:#4caf50,stroke-width:2px,color:black
    style ExperienceExtractor fill:#e1f5fe,stroke:#03a9f4,stroke-width:2px,color:black
    style EducationExtractor fill:#e1f5fe,stroke:#03a9f4,stroke-width:2px,color:black

    class BaseExtractor {
        +Selector selector
        +extract_with_fallback(field, xpaths)
        +extract_list(xpaths)
    }

    class Registry {
        +dict SELECTORS
    }

    class HeaderExtractor {
        +extract()
    }
    
    class MetricsExtractor {
        +extract()
    }
    
    class SectionExtractor {
        -_get_section_root(headers)
        +extract_section(names)
    }

    class ExperienceExtractor {
        +extract()
    }

    class EducationExtractor {
        +extract()
    }

    BaseExtractor <|-- HeaderExtractor
    BaseExtractor <|-- MetricsExtractor
    BaseExtractor <|-- SectionExtractor
    SectionExtractor <|-- ExperienceExtractor
    SectionExtractor <|-- EducationExtractor
    
    BaseExtractor ..> Registry : Uses XPaths
```

### 3. Execution Sequence Diagram
This diagram visualizes the runtime execution flow when `extract_profile.py` is triggered.

```mermaid
sequenceDiagram
    autonumber
    
    participant Main as Main Script
    participant FS as File System
    participant Engine as Extraction Engine
    participant Header as HeaderExtractor
    participant Exp as ExperienceExtractor
    participant Reg as Selector Registry

    note over Main, FS: Initialization
    Main->>FS: List *.html files
    FS-->>Main: [profile1.html, profile2.html]
    
    loop For each file
        Main->>FS: Read content
        FS-->>Main: HTML String
        Main->>Engine: extract_data_from_html(html)
        
        rect rgb(220, 240, 220)
            note right of Engine: Header Extraction
            Engine->>Header: extract()
            Header->>Reg: Get "header" selectors
            Header-->>Engine: {name, headline, ...}
        end
        
        rect rgb(220, 220, 240)
            note right of Engine: Experience Extraction
            Engine->>Exp: extract()
            Exp->>Reg: Get "section" selectors
            Exp-->>Engine: [{title, company, ...}, ...]
        end
        
        Engine-->>Main: User Data Dict
    end
    
    Main->>FS: Write profile.json
```
