# EasyParkPlus - Parking Lot Manager (Refactored)

## Project Overview
This is the refactored EasyParkPlus parking lot management prototype, submitted for Project 3: Software Design.

## Quick Start

### Running the Application
```bash
cd refactored_code
python3 AppGUI.py
```

### Running Tests
```bash
cd refactored_code
python3 -m unittest test_ParkingManager -v
```

## Project Structure
```
project_3_software_design/
├── README.md
├── assets/
│   └── Screenshot 2026-05-24 161746.png
├── docs/
│   ├── 07_Interview_Questions_for_Technical_Manager.md
│   ├── implementations/
│   │   ├── 08_Domain_Driven_Design.md
│   │   ├── 09_Refactoring_Justification.md
│   │   ├── 10_Microservices_Architecture.md
│   │   ├── 11_UML_Diagrams.md
│   │   └── 12_Mock_Implementation_vs_Manager_Requirements.md
│   └── requirements/
│       ├── 01_Project_Overview.md
│       ├── 02_Refactoring_Requirements.md
│       ├── 03_Domain_Driven_Design_Requirements.md
│       ├── 04_Microservices_Architecture_Requirements.md
│       ├── 05_Submission_Guidelines.md
│       ├── 06_Rubric.md
│       └── rubrics.pdf
├── legacy_code/
│   ├── ElectricVehicle.py     # Original EV classes (broken inheritance)
│   ├── ParkingManager.py      # Original monolithic prototype
│   └── Vehicle.py             # Original vehicle classes
├── refactored_code/
│   ├── AppGUI.py              # Tkinter GUI (Observer subscriber)
│   ├── ElectricVehicle.py     # EV vehicle hierarchy
│   ├── ParkingManager.py      # Core domain logic (Observer publisher)
│   ├── Vehicle.py             # Base vehicle hierarchy
│   ├── VehicleFactory.py      # Factory Method pattern implementation
│   └── test_ParkingManager.py # Unit tests (50 tests)
└── uml_diagrams/
    ├── original_class_diagram.png
    ├── original_sequence_diagram.png
    ├── refactored_class_diagram.png
    └── refactored_sequence_diagram.png
```

## Design Patterns Used
1. **Factory Method** - `VehicleFactory.create_vehicle()` centralizes vehicle instantiation, eliminating tight coupling between `ParkingLot` and concrete vehicle classes.
2. **Observer** - `ParkingLot` publishes trace events via `add_trace_observer()`, allowing the GUI and other components to subscribe to domain-level notifications without direct coupling.

## Key Improvements
- Removed global variables and extracted GUI into `AppGUI` class
- Fixed broken inheritance (`ElectricCar`/`ElectricBike` now properly extend `ElectricVehicle` which extends `Vehicle`)
- Consolidated 8 copy-paste query methods into 4 parameterized methods
- Added input validation (empty regnum, duplicate detection, bounds checking)
- Replaced `-1` sentinel values with semantically correct `None`
- Removed dead code (`edit()`, unused imports, unreachable returns)

## Requirements
- Python 3.x
- Tkinter (usually bundled with Python)
