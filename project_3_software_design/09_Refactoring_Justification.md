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
    - **Fix**: Consolidated multiple copy-pasted redundant methods into flexible list comprehensions. E.g., a single method handles filtering based on EV/non-EV flags.
6. **Unnecessary Abstractions & Broken Inheritance**: `ElectricCar` called `ElectricVehicle.__init__` but failed to formally declare class inheritance `class ElectricCar(ElectricVehicle):`.
    - **Fix**: Corrected the inheritance chain and removed unpythonic Java-style getter methods, relying instead on direct property access.

## Implemented Design Patterns

### 1. Factory Method Pattern
In the original `ParkingManager.py`, the `park()` method contained deeply nested and confusing `if/else` logic specifically for instantiating different types of vehicles (`ElectricBike`, `ElectricCar`, `Car`, `Motorcycle`) based on boolean flags.

**Implementation**: We extracted this instantiation logic into the `VehicleFactory` class. The factory provides a single static interface `VehicleFactory.create_vehicle(is_ev, is_motorcycle, ...)` that encapsulates the decision-making process. This improves modularity and adhering to the Single Responsibility Principle, as the `ParkingLot` no longer needs to know exactly how to construct the vehicles.

### 2. Singleton Pattern
In the original application, the `ParkingLot` instance was initialized in `main()` and strictly bound to the local GUI lifecycle. In a larger, realistic architecture where other components (e.g., a background task, an external API, or additional UI windows) need access to the core parking lot state, passing the variable around would become cumbersome and risky.

**Implementation**: The `ParkingLot` class was refactored to implement the Singleton pattern using the `__new__` dunder method. This ensures that no matter how many times `ParkingLot()` is instantiated in the system, it will always return the exact same memory instance. This guarantees a single, consistent source of truth for the parking inventory state.
