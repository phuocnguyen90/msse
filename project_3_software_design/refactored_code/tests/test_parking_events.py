"""
Unit tests for the Event-Driven Architecture (Domain Events) in ParkingLot.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ParkingManager import ParkingLot
from DomainEvents import LotInitializedEvent, VehicleParkedEvent, VehicleDepartedEvent


class TestParkingEvents(unittest.TestCase):
    """Test suite for verifying that the ParkingLot acts as an event publisher."""

    def test_tracing_create_and_park(self):
        """Verify that LotInitializedEvent and VehicleParkedEvent are published during creation and parking."""
        traced_events = []
        def mock_event(event):
            traced_events.append(event)

        lot = ParkingLot()
        lot.add_event_observer(mock_event)
        lot.createParkingLot(capacity=1, evcapacity=0, level=1)
        lot.park("REG1", "Honda", "Civic", "Red", False, False)

        self.assertGreater(len(traced_events), 0)
        self.assertTrue(any(isinstance(e, LotInitializedEvent) for e in traced_events))
        self.assertTrue(any(isinstance(e, VehicleParkedEvent) for e in traced_events))

    def test_tracing_leave(self):
        """Verify that VehicleDepartedEvent is published when a vehicle leaves."""
        traced_events = []
        def mock_event(event):
            traced_events.append(event)

        lot = ParkingLot()
        lot.add_event_observer(mock_event)
        lot.createParkingLot(capacity=1, evcapacity=0, level=1)
        lot.park("REG1", "Honda", "Civic", "Red", False, False)
        lot.leave(1, False)

        self.assertTrue(any(isinstance(e, VehicleDepartedEvent) for e in traced_events))

    def test_event_observers_are_instance_scoped(self):
        """Verify that different ParkingLot instances do not share event observers."""
        lot1 = ParkingLot()
        lot2 = ParkingLot()
        
        first_trace = []
        second_trace = []
        
        lot1.add_event_observer(first_trace.append)
        lot2.add_event_observer(second_trace.append)

        lot1.createParkingLot(capacity=1, evcapacity=0, level=1)
        lot2.createParkingLot(capacity=1, evcapacity=0, level=2)

        self.assertEqual(len(first_trace), 1)
        self.assertEqual(len(second_trace), 1)
        self.assertEqual(first_trace[0].level, 1)
        self.assertEqual(second_trace[0].level, 2)

if __name__ == '__main__':
    unittest.main()
