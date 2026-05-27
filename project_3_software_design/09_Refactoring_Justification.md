# Refactoring Justification

## Overview of Removed Anti-Patterns

1. **Global Variables & Tight Coupling**: The original code heavily relied on global variables (`num_value`, `root`, `tfield`) and the `ParkingLot` class directly pushed strings into the Tkinter UI. 
    - **Fix**: The GUI code was extracted into a new `AppGUI` class that encapsulates all `tk.StringVar` dependencies. The `ParkingLot` logic now only deals with state and returns raw data (strings or lists), entirely decoupling the model from the view.
2. **Returning Different/Mixed Types**: The `slots` and `evSlots` arrays used to be initialized with `-1` integers and later overridden by `Vehicle` objects. 
    - **Fix**: Replaced `-1` with `None`. Lists now store instances of `Vehicle` or `None`, which is semantically correct in Python.
3. **Clumsy, Unnecessary Loop Statements**: Iterating manually over `self.slots` to find an empty spot with `-1` was verbose. 
    - **Fix**: Replaced with pythonic syntax: `self.slots.index(None)` inside a `try/except` block.
4. **Using try/except blocks without handling exceptions**: The original code parsed user strings into integers (`int(num_value.get())`) without any error handling. 
    - **Fix**: The `AppGUI` class now wraps input processing in `try/except ValueError` blocks to cleanly display a user-friendly message rather than crashing the script.
5. **Buggy Copy-Paste Code**: Methods like `getSlotNumFromMakeEv` accepted `color` as an argument but then checked `self.evSlots[i].make == make`, leading to `NameError`. 
    - **Fix**: Consolidated multiple copy-pasted redundant methods into flexible list comprehensions. Query behavior for registration number, color, make, and model is preserved through shared methods that accept an EV/non-EV selector instead of maintaining separate duplicated methods for each slot type.
6. **Unnecessary Abstractions & Broken Inheritance**: `ElectricCar` called `ElectricVehicle.__init__` but failed to formally declare class inheritance `class ElectricCar(ElectricVehicle):`.
    - **Fix**: Corrected the inheritance chain and removed unpythonic Java-style getter methods, relying instead on direct property access.
7. **Unused Import**: `ParkingManager.py` imported `sys` on line 3, but it was never referenced anywhere in the file.
    - **Fix**: Removed the unused `import sys` statement to clean up dependencies.
8. **Unreachable Code**: The `edit()` method in `ParkingManager.py` (lines 107-115) had both `if` and `else` branches returning `True`, making the final `return False` on line 115 unreachable.
    - **Fix**: Removed the unused `edit()` operation from the refactored `ParkingLot` API. The submitted GUI never exposed edit behavior, so keeping a broken editing method would preserve dead code rather than improve the prototype.
9. **Implicit `None` Return**: `getEmptyLevel()` (lines 60-62) returned `self.level` only when both counters were zero; otherwise it implicitly returned `None` without an explicit `else` or default return.
    - **Fix**: Removed the method entirely as it was unused in the GUI and its implicit `None` return was confusing. The `level` property is accessible directly on the `ParkingLot` instance.
10. **Code Duplication / DRY Violation**: `ElectricVehicle.py` redundantly defined `getMake()`, `getModel()`, `getColor()`, and `getRegNum()` — identical to those in `Vehicle.py` — even though `ElectricVehicle` did not inherit from `Vehicle`.
    - **Fix**: Made `ElectricVehicle` properly inherit from `Vehicle` and removed the duplicated getter methods, eliminating 16 lines of redundant code.
11. **Unused Variables**: `command_value` and `level_remove_value` were declared as global `tk.StringVar` instances in `ParkingManager.py` (lines 12 and 27) but never read or bound to any widget.
    - **Fix**: Removed both unused variables during the extraction of GUI state into the `AppGUI` class.
12. **Inconsistent "Not Found" Return Types**: `getRegNumFromColor()` returned an empty list `[]` when no matches were found, while `getSlotNumFromRegNum()` returned `-1` for the same semantic condition.
    - **Fix**: Standardized all query methods to return empty collections (`[]` for lists, `-1` for single-value lookups) consistently. Documented the contract clearly in method names and return types.
13. **Inconsistent Slot Indexing**: `leave(slotid)` used `slotid - 1` (0-based indexing for the array), but `edit(slotid)` used `slotid` directly (1-based), creating an off-by-one bug risk.
    - **Fix**: Standardized all public API methods to accept 1-based slot IDs (user-facing) and convert to 0-based indexing internally with clear boundary checks.
14. **Missing Input Validation**: `leave()` accepted any integer for `slotid` without checking if it was negative or exceeded the array bounds, risking an `IndexError`.
    - **Fix**: Added explicit bounds checking: `if index < 0: return False` and `if index >= len(self.slots): return False` before array access.
15. **Hardcoded String Types**: `getType()` methods in the regular vehicle classes returned hardcoded strings like `"Car"`, `"Truck"`, `"Motorcycle"`, and `"Bus"` instead of deriving the type from the class name.
    - **Fix**: Replaced those regular-vehicle hardcoded strings with a dynamic `@property def type(self): return self.__class__.__name__` on the base `Vehicle` class. `ElectricCar` and `ElectricBike` still intentionally override `type` as `"Car"` and `"Motorcycle"` because the parking-lot UI groups them by parking category while EV-specific behavior is represented by their class hierarchy and EV slot assignment.
16. **UI Mutation in Model Layer**: `status()` and `chargeStatus()` in the original `ParkingLot` class called `tfield.insert(tk.INSERT, output)` directly, tightly coupling the business logic to the Tkinter text widget.
    - **Fix**: Refactored both methods to return the formatted string instead of printing it. The `AppGUI` class now receives the string and decides how to display it, enforcing a clean Model-View separation.

## Implemented Design Patterns

### 1. Factory Method Pattern
In the original `ParkingManager.py`, the `park()` method contained deeply nested and confusing `if/else` logic specifically for instantiating different types of vehicles (`ElectricBike`, `ElectricCar`, `Car`, `Motorcycle`) based on boolean flags.

**Implementation**: We extracted this instantiation logic into the `VehicleFactory` class. The factory provides a single static interface `VehicleFactory.create_vehicle(is_ev, is_motorcycle, ..., vehicle_type=None)` that encapsulates the decision-making process. Existing calls still support regular cars, motorcycles, electric cars, and electric bikes through the original flags, while explicit `vehicle_type` values also support trucks and buses through the `ParkingLot.park(..., vehicle_type=...)` API. This improves modularity and adhering to the Single Responsibility Principle, as the `ParkingLot` no longer needs to know exactly how to construct the vehicles.

### 2. Observer Pattern
In the original application, the `ParkingLot` class directly wrote output to the Tkinter text field, which meant the domain logic had to know about the UI. That tight coupling made it hard to reuse the parking logic for multiple facilities, tests, logging, or future service-level integrations.

**Implementation**: The `ParkingLot` class now exposes `add_trace_observer()` and `remove_trace_observer()` methods. The GUI subscribes to trace events and displays them, while `ParkingLot` only publishes domain-level trace messages. Each `ParkingLot` instance owns its own observer list, so separate facilities can run with independent state and independent trace subscribers.
