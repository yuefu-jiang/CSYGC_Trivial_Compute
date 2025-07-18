# CSYGC Trivial Compute - Server Design Document

## Overview

The CSYGC Trivial Compute server is a Python-based Flask web server that manages a trivia board game similar to Trivial Pursuit. The server handles game instances, player management, board state, question serving, and game logic through a RESTful API.

## Architecture Overview

```mermaid
graph TB
    A[Electron Frontend] --> B[Flask Server]
    B --> C[Game Instance Manager]
    B --> D[Question Database]
    C --> E[Game Objects]
    E --> F[Trivial Board]
    E --> G[Tokens]
    E --> H[Wedges]
    
    subgraph "Server Components"
        B
        C
        D
    end
    
    subgraph "Game Logic"
        E
        F
        G
        H
    end
```

## System Components

### 1. Server Module (`server.py`)

**Purpose**: Main Flask application server that handles HTTP requests and manages game sessions.

**Key Responsibilities**:
- HTTP API endpoint management
- CORS configuration for cross-origin requests
- Game session storage and management
- Question database interaction
- Logging and debugging

**API Endpoints**:
- `POST /rule` - Test endpoint returning basic message
- `GET /question` - Retrieve specific question by category and ID
- `POST /init_questions` - Initialize and return all available questions
- `POST /initializegametest` - Create new game instance

```mermaid
sequenceDiagram
    participant Client
    participant Server
    participant GameInstance
    participant QuestionDB
    
    Client->>Server: POST /initializegametest
    Server->>GameInstance: create new instance
    GameInstance->>GameInstance: initialize board & tokens
    Server->>Server: store in gameSession
    Server-->>Client: success response
    
    Client->>Server: GET /question?category=science&qid=Q001
    Server->>QuestionDB: load questions.json
    QuestionDB-->>Server: question data
    Server-->>Client: question response
```

### 2. Game Instance Module (`gameinstance.py`)

**Purpose**: Main game controller that manages individual game sessions.

**Key Components**:
- Game board creation and management
- Player token initialization
- Board coloring assignment
- Token movement and positioning

```mermaid
classDiagram
    class GameInstance {
        -gboard: Trivialboard
        -gameid: str
        -boardsize: int
        -playerno: int
        -tokenlist: list[Token]
        -wedgelist: Wedge
        +initialize(gameid, playerlist, q_type, b_size)
        +coloring()
        +currentpos(name) list
        +showdest(tid, steps) list
        +movetoken(tid, location)
    }
    
    GameInstance --> Trivialboard
    GameInstance --> Token
    GameInstance --> Wedge
```

### 3. Game Objects Module (`gameobject.py`)

**Purpose**: Core game entities and their behaviors.

#### Class Hierarchy

```mermaid
classDiagram
    class Wedge {
        +chosen: set
        +size: int
        +__init__(in_size)
    }
    
    class Token {
        +label: str
        +row: int
        +col: int
        +missing: set
        +collection: set
        +score: int
        +HqOk: bool
        +CenterOk: bool
        +full: bool
        +__init__(wedge)
        +addw(item)
    }
    
    class Square {
        +valid: bool
        +cat: str
        +color: str
        +__init__(valid, cat)
    }
    
    class Trivialboard {
        +CT: list
        +board: list[list[Square]]
        +__init__(size_in)
        +createboard(size) list
        +print_b()
    }
    
    Token --> Wedge : uses
    Trivialboard --> Square : contains
```

#### Board Layout

The game board is a 9x9 grid with special squares:

```
     0   1   2   3   4   5   6   7   8   
  0 [RA][NL][NL][NL][HQ][NL][NL][NL][RA]
  1 [NL][  ][  ][  ][NL][  ][  ][  ][NL]
  2 [NL][  ][  ][  ][NL][  ][  ][  ][NL]
  3 [NL][  ][  ][  ][NL][  ][  ][  ][NL]
  4 [HQ][NL][NL][NL][CT][NL][NL][NL][HQ]
  5 [NL][  ][  ][  ][NL][  ][  ][  ][NL]
  6 [NL][  ][  ][  ][NL][  ][  ][  ][NL]
  7 [NL][  ][  ][  ][NL][  ][  ][  ][NL]
  8 [RA][NL][NL][NL][HQ][NL][NL][NL][RA]
```

**Square Types**:
- `CT`: Center (starting position)
- `HQ`: Headquarters (special squares for each color)
- `RA`: Roll Again squares
- `NL`: Normal colored squares
- `IV`: Invalid squares (empty spaces)

### 4. Game Helper Functions (`gamehelperfunct.py`)

**Purpose**: Utility functions for game mechanics.

**Functions**:
- `rolldice(x=1)`: Simulates dice rolling
- `destination(row, col, steps, board)`: Calculates possible moves
- `printlist(plist)`: Debug utility for board printing

```mermaid
graph LR
    A[Current Position] --> B[Calculate Destinations]
    B --> C[Valid Adjacent Squares]
    C --> D[Recursive Movement]
    D --> E[Return Possible Positions]
    
    F[Dice Roll] --> G[Movement Steps]
    G --> B
```

## Data Flow Architecture

```mermaid
graph TD
    A[Client Request] --> B[Flask Router]
    B --> C{Route Type}
    C -->|Game Init| D[GameInstance.initialize]
    C -->|Question| E[Question Manager]
    C -->|Move| F[Token Movement]
    
    D --> G[Create Board]
    D --> H[Create Tokens]
    D --> I[Assign Colors]
    
    E --> J[Load questions.json]
    J --> K[Return Question Data]
    
    F --> L[Calculate Destinations]
    F --> M[Update Token Position]
    
    G --> N[Store in gameSession]
    H --> N
    I --> N
    K --> O[JSON Response]
    M --> O
```

## Question Management System

The server manages a JSON-based question database with the following structure:

```json
{
  "category": {
    "question_id": {
      "question": "Question text",
      "answer": "Answer text",
      "used": false
    }
  }
}
```

**Categories**: science, history, sports, entertainment, geography, etc.

```mermaid
erDiagram
    QUESTION_DATABASE ||--o{ CATEGORY : contains
    CATEGORY ||--o{ QUESTION : has
    QUESTION {
        string question_id PK
        string question
        string answer
        boolean used
    }
    CATEGORY {
        string name PK
    }
```

## Game State Management

### Session Storage

```mermaid
graph LR
    A[gameSession Dictionary] --> B[Game ID]
    B --> C[GameInstance Object]
    C --> D[Board State]
    C --> E[Player Tokens]
    C --> F[Game Configuration]
```

### Token State Tracking

```mermaid
stateDiagram-v2
    [*] --> Initialized
    Initialized --> Moving : dice_roll
    Moving --> Positioned : move_complete
    Positioned --> AnsweringQuestion : land_on_square
    AnsweringQuestion --> WedgeEarned : correct_answer
    AnsweringQuestion --> Positioned : incorrect_answer
    WedgeEarned --> Positioned : continue_game
    Positioned --> GameWon : all_wedges_collected
    GameWon --> [*]
```

## API Design

### Request/Response Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant G as GameInstance
    participant Q as QuestionDB
    
    Note over C,Q: Game Initialization
    C->>S: POST /initializegametest
    S->>G: new GameInstance()
    G->>G: initialize(gameid, players)
    S->>S: store in gameSession
    S-->>C: {data: "success", list: [0,1]}
    
    Note over C,Q: Question Retrieval
    C->>S: GET /question?category=science&qid=Q001
    S->>Q: load questions.json
    Q-->>S: question data
    S-->>C: {category, qid, data: {...}}
    
    Note over C,Q: Movement (Future Implementation)
    C->>S: POST /move
    S->>G: showdest(token_id, steps)
    G-->>S: possible_destinations[]
    S->>G: movetoken(token_id, location)
    S-->>C: {new_position, square_type}
```

## Error Handling and Logging

The server implements comprehensive logging and error handling:

```python
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s  %(message)s'
)
```

**Error Scenarios**:
- Missing question parameters
- Question not found
- Game initialization failures
- Invalid move requests

## Performance Considerations

### Memory Management
- Game sessions stored in memory dictionary
- Question database loaded per request (could be optimized)
- Board state maintained efficiently with 2D arrays

### Scalability
- Current implementation supports single-server deployment
- Session storage in memory limits horizontal scaling
- Future improvements could include:
  - Database-backed session storage
  - Redis for session management
  - Stateless API design

## Security Considerations

### Current Implementation
- CORS enabled for cross-origin requests
- No authentication/authorization implemented
- No input validation on API endpoints

### Recommendations
- Add input validation and sanitization
- Implement rate limiting
- Add authentication for game sessions
- Validate game state transitions

## Deployment Architecture

```mermaid
graph TB
    A[Electron App] --> B[Embedded Flask Server]
    B --> C[Local File System]
    C --> D[questions.json]
    C --> E[Python Modules]
    
    subgraph "Local Deployment"
        B
        C
        D
        E
    end
    
    F[Process Manager] --> B
    F --> G[Port: 5000 (configurable)]
```

## Future Enhancements

### Planned Features
1. **Complete Movement API**: Full implementation of token movement endpoints
2. **Game Rules Engine**: Answer validation and wedge collection logic
3. **Real-time Updates**: WebSocket support for multi-player synchronization
4. **Persistence**: Database integration for game state persistence
5. **Admin Interface**: Game management and question database administration

### Technical Debt
1. **Error Handling**: Improve comprehensive error handling across all modules
2. **Input Validation**: Add request validation and sanitization
3. **Testing**: Implement unit and integration tests
4. **Documentation**: Add inline code documentation and API specs
5. **Configuration**: Externalize configuration settings

## Conclusion

The CSYGC Trivial Compute server provides a solid foundation for a trivia board game with a clean separation of concerns between web serving, game logic, and data management. The modular design allows for easy extension and maintenance while the Flask framework provides a reliable web server foundation.

The current implementation focuses on core game mechanics and basic API endpoints, with room for enhancement in areas such as real-time communication, persistence, and advanced game features.