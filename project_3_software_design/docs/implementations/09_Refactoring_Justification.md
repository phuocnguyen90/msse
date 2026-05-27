# Refactoring Justification

The original codebase had problems at several different levels. Some issues were **paradigm-level OOP problems**, where the code did not use object-oriented design principles effectively. Some were recognizable **design anti-patterns**, where responsibilities were arranged in a recurring but harmful structure. Others were smaller **code smells** or concrete **defect risks**. Separating these categories makes the refactoring rationale clearer than treating every issue as an "anti-pattern."

## 1. Paradigm-Level OOP Problems

These issues reflect weaknesses in how the legacy code applied object-oriented design.

1. **Poor Object-Oriented Responsibility Assignment**: The legacy `ParkingLot` class and `ParkingManager.py` module collapsed domain state, use-case orchestration, object creation, UI control, output formatting, and direct Tkinter mutation into one place. This made `ParkingLot` low-cohesion and difficult to test or extend.
    - **Fix / Remaining Limitation**: The refactor split the most problematic responsibilities across clearer objects. `AppGUI` owns Tkinter state and display behavior. `VehicleFactory` owns vehicle creation. The observer trace mechanism handles notification without forcing the domain logic to know about Tkinter widgets. `ParkingLot` now focuses on parking state and use-case methods, but it still also contains query helpers and report-string formatting (`status()` and `chargeStatus()`). A stricter layered design would move reporting/formatting into a presenter or application service.
2. **Concrete-Class Coupling / Missing Creation Abstraction**: The original `park()` method directly instantiated `ElectricCar`, `ElectricBike`, `Car`, and `Motorcycle` inside the parking workflow.
    - **Fix**: Vehicle creation was moved behind `VehicleFactory.create_vehicle(...)`, so `ParkingLot` no longer needs to know how each concrete vehicle class is constructed.
3. **Broken Inheritance**: `ElectricCar` and `ElectricBike` called `ElectricVehicle.__init__`, but they did not formally inherit from `ElectricVehicle`.
    - **Fix**: Corrected the inheritance chain with `class ElectricCar(ElectricVehicle)` and `class ElectricBike(ElectricVehicle)`.
4. **Primitive Flags and Sentinel Values Instead of Clearer Domain Concepts**: The legacy design relied heavily on `ev`, `motor`, raw slot IDs, raw strings, and `-1` sentinels to represent domain concepts.
    - **Partial Fix**: The refactor reduces this problem by using `None` for empty slots, adding `vehicle_type` support in the factory, and clarifying query contracts. It does not fully eliminate primitive/domain-value modeling because `ev`, `motor`, raw slot IDs, and strings are still part of the public API and GUI workflow. A larger production design would go further by introducing richer value objects such as `VehicleType`, `ParkingSession`, and `SlotStatus`.

## 2. Design Anti-Patterns

These are recurring harmful design structures in the legacy implementation.

5. **Smart UI / Missing Application Service Boundary**: The original code heavily relied on global Tkinter variables (`num_value`, `root`, `tfield`), and the `ParkingLot` class directly read UI state and mutated the Tkinter text widget. Methods such as `status()` and `chargeStatus()` called `tfield.insert(...)`, which meant the domain model knew about the presentation layer.
    - **Fix / Remaining Limitation**: The GUI code was extracted into `AppGUI`, and `ParkingLot` no longer imports or mutates Tkinter widgets. `ParkingLot` now returns result data or formatted strings, and the GUI decides where to display them. However, because `status()` and `chargeStatus()` still build display-oriented strings, this is a partial Model-View separation rather than a fully clean presentation/domain split.
6. **God Object Tendency**: `ParkingLot` was not a full God Object, but it was moving in that direction because it handled parking state, vehicle construction, query behavior, output formatting, and UI callbacks.
    - **Partial Fix**: The refactor moves creation logic to `VehicleFactory`, UI display behavior to `AppGUI`, and trace notification to an observer mechanism. `ParkingLot` is smaller and more testable, but it still carries parking state, use-case methods, query helpers, and report-string formatting, so the God Object tendency is reduced rather than completely eliminated.

## 3. Maintainability and Code Quality Issues

These are poor coding practices that reduce maintainability, violate clean code principles (like DRY), or use language features incorrectly.

7. **Mixed Sentinel Values and Domain Objects**: The `slots` and `evSlots` arrays used to be initialized with `-1` integers and later overwritten with `Vehicle` objects.
    - **Fix**: Replaced `-1` with `None`. Lists now store instances of `Vehicle` or `None`, which is semantically correct in Python.
8. **Verbose Slot-Search Loops**: The original code manually iterated over slot arrays to find an empty spot.
    - **Fix**: Replaced with pythonic syntax: `self.slots.index(None)` inside a `try/except` block.
9. **Code Duplication / DRY Violation**: `ElectricVehicle.py` redundantly defined `getMake()`, `getModel()`, `getColor()`, and `getRegNum()` — identical to those in `Vehicle.py` — even though `ElectricVehicle` did not inherit from `Vehicle`.
    - **Fix**: Made `ElectricVehicle` properly inherit from `Vehicle` and removed the duplicated getter methods, eliminating 16 lines of redundant code.
10. **Dead or Confusing Helper Method**: `getEmptyLevel()` returned `self.level` only when both counters were zero; otherwise it implicitly returned `None`. It was also unused by the GUI.
    - **Fix**: Removed the method entirely as it was unused in the GUI and its implicit `None` return was confusing. The `level` property is accessible directly on the `ParkingLot` instance.
11. **Duplicated Query APIs with Unclear Contracts**: The original code duplicated query methods for regular and EV slots (`getSlotNumFromColor` vs. `getSlotNumFromColorEv`, etc.). The API also mixed list-returning queries with single-value lookups without making the contract explicit.
    - **Fix**: Consolidated the duplicated query methods into shared implementations that accept an EV/non-EV selector. List-based queries return empty lists when no matches exist, while single-slot lookup returns `-1` when no match exists.
12. **Hardcoded String Types**: `getType()` methods in the regular vehicle classes returned hardcoded strings like `"Car"`, `"Truck"`, `"Motorcycle"`, and `"Bus"` instead of deriving the type from the class name.
    - **Fix**: Replaced those regular-vehicle hardcoded strings with a dynamic `@property def type(self): return self.__class__.__name__` on the base `Vehicle` class. `ElectricCar` and `ElectricBike` still intentionally override `type` as `"Car"` and `"Motorcycle"` because the parking-lot UI groups them by parking category while EV-specific behavior is represented by their class hierarchy and EV slot assignment.
13. **Unused Variables**: `command_value` and `level_remove_value` were declared as global `tk.StringVar` instances in `ParkingManager.py` but never read or bound to any widget.
    - **Fix**: Removed both unused variables during the extraction of GUI state into the `AppGUI` class.
14. **Unused Import**: `legacy_code/ParkingManager.py` imported `sys`, but it was never referenced anywhere in the file.
    - **Fix**: Removed the unused `import sys` statement to clean up dependencies.

## 4. Bugs & Defect Risks

These are outright logic errors, unhandled exceptions, and missing validations that could cause runtime crashes or incorrect behavior.

15. **Buggy Copy-Paste Code**: Methods like `getSlotNumFromMakeEv` accepted `color` as an argument but then checked `self.evSlots[i].make == make`, leading to `NameError`.
    - **Fix**: Consolidated multiple copy-pasted redundant methods into flexible list comprehensions. Query behavior for registration number, color, make, and model is preserved through shared methods that accept an EV/non-EV selector instead of maintaining separate duplicated methods for each slot type.
16. **Inverted Regular Vehicle Creation**: In `legacy_code/ParkingManager.py`, the regular parking branch created a `Vehicle.Car` when `motor == 1` and a `Vehicle.Motorcycle` otherwise. This inverted the meaning of the motorcycle flag for non-EV vehicles.
    - **Fix**: Vehicle creation now goes through `VehicleFactory.create_vehicle()`, where `is_motorcycle=True` consistently creates a motorcycle and `is_motorcycle=False` creates a car unless an explicit `vehicle_type` such as `truck` or `bus` is provided.
17. **Unhandled Input Conversion Errors**: The original code parsed user strings into integers (`int(num_value.get())`) without handling invalid user input.
    - **Fix**: The `AppGUI` class now wraps input processing in `try/except ValueError` blocks to cleanly display a user-friendly message rather than crashing the script.
18. **Unreachable Code**: The `edit()` method in `legacy_code/ParkingManager.py` had both `if` and `else` branches returning `True`, making the final `return False` unreachable.
    - **Fix**: Removed the unused `edit()` operation from the refactored `ParkingLot` API. The submitted GUI never exposed edit behavior, so keeping a broken editing method would preserve dead code rather than improve the prototype.
19. **Inconsistent Slot Indexing**: `leave(slotid)` used `slotid - 1` (0-based indexing for the array), but `edit(slotid)` used `slotid` directly (1-based), creating an off-by-one bug risk.
    - **Fix**: Standardized all public API methods to accept 1-based slot IDs (user-facing) and convert to 0-based indexing internally with clear boundary checks.
20. **Missing Slot Bounds Validation**: `leave()` accepted any integer for `slotid` without checking if it was negative or exceeded the array bounds, risking an `IndexError`.
    - **Fix**: Added explicit bounds checking: `if index < 0: return False` and `if index >= len(self.slots): return False` before array access.

## Implemented Design Patterns

### 1. Simple Factory / Factory Method-Style Pattern
In the original `ParkingManager.py`, the `park()` method contained deeply nested and confusing `if/else` logic specifically for instantiating different types of vehicles (`ElectricBike`, `ElectricCar`, `Car`, `Motorcycle`) based on boolean flags.

**Implementation**: We extracted this instantiation logic into the `VehicleFactory` class. Technically, the implementation is closer to a **Simple Factory** than the strict GoF Factory Method pattern because it uses a centralized static creator rather than subclass-defined factory methods. It still serves the intended object-creation-pattern role for this project by providing a single interface, `VehicleFactory.create_vehicle(is_ev, is_motorcycle, ..., vehicle_type=None)`, that encapsulates the decision-making process. Existing calls still support regular cars, motorcycles, electric cars, and electric bikes through the original flags, while explicit `vehicle_type` values also support trucks and buses through the `ParkingLot.park(..., vehicle_type=...)` API. This improves modularity and adherence to the Single Responsibility Principle because `ParkingLot` no longer directly constructs every vehicle class.

### 2. Observer Pattern
In the original application, the `ParkingLot` class directly wrote output to the Tkinter text field, which meant the domain logic had to know about the UI. That tight coupling made it hard to reuse the parking logic for multiple facilities, tests, logging, or future service-level integrations.

**Implementation**: The `ParkingLot` class now exposes `add_trace_observer()` and `remove_trace_observer()` methods. The GUI subscribes to trace events and displays them, while `ParkingLot` only publishes domain-level trace messages. Each `ParkingLot` instance owns its own observer list, so separate facilities can run with independent state and independent trace subscribers.
