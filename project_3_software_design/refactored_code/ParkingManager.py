import tkinter as tk
from VehicleFactory import VehicleFactory

class ParkingLot:
    """
    Singleton Pattern: Ensures only one instance of the ParkingLot exists.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ParkingLot, cls).__new__(cls, *args, **kwargs)
            cls._instance.capacity = 0
            cls._instance.evCapacity = 0
            cls._instance.level = 0
            cls._instance.numOfOccupiedSlots = 0
            cls._instance.numOfOccupiedEvSlots = 0
            cls._instance.slots = []
            cls._instance.evSlots = []
        return cls._instance

    def createParkingLot(self, capacity, evcapacity, level):
        self.capacity = capacity
        self.evCapacity = evcapacity
        self.level = level
        # Using None instead of -1 for empty slots to prevent mixed types (int vs Vehicle)
        self.slots = [None] * capacity
        self.evSlots = [None] * evcapacity
        self.numOfOccupiedSlots = 0
        self.numOfOccupiedEvSlots = 0
        return self.level

    def getEmptySlot(self):
        try:
            return self.slots.index(None)
        except ValueError:
            return -1

    def getEmptyEvSlot(self):
        try:
            return self.evSlots.index(None)
        except ValueError:
            return -1

    def park(self, regnum, make, model, color, ev, motor):
        if ev:
            if self.numOfOccupiedEvSlots < self.evCapacity:
                slotid = self.getEmptyEvSlot()
                if slotid != -1:
                    self.evSlots[slotid] = VehicleFactory.create_vehicle(True, motor, regnum, make, model, color)
                    self.numOfOccupiedEvSlots += 1
                    return slotid + 1  # 1-based index for user
            return -1
        else:
            if self.numOfOccupiedSlots < self.capacity:
                slotid = self.getEmptySlot()
                if slotid != -1:
                    self.slots[slotid] = VehicleFactory.create_vehicle(False, motor, regnum, make, model, color)
                    self.numOfOccupiedSlots += 1
                    return slotid + 1
            return -1

    def leave(self, slotid, ev):
        index = slotid - 1
        if index < 0:
            return False

        if ev:
            if index < len(self.evSlots) and self.evSlots[index] is not None:
                self.evSlots[index] = None
                self.numOfOccupiedEvSlots -= 1
                return True
        else:
            if index < len(self.slots) and self.slots[index] is not None:
                self.slots[index] = None
                self.numOfOccupiedSlots -= 1
                return True
        return False

    def status(self):
        output = "Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\n"
        for i, v in enumerate(self.slots):
            if v is not None:
                output += f"{i+1}\t{self.level}\t{v.regnum}\t\t{v.color}\t\t{v.make}\t\t{v.model}\n"
            
        output += "\nElectric Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\n"
        for i, ev in enumerate(self.evSlots):
            if ev is not None:
                output += f"{i+1}\t{self.level}\t{ev.regnum}\t\t{ev.color}\t\t{ev.make}\t\t{ev.model}\n"
        return output

    def chargeStatus(self):
        output = "Electric Vehicle Charge Levels\nSlot\tFloor\tReg No.\t\tCharge %\n"
        for i, ev in enumerate(self.evSlots):
            if ev is not None:
                output += f"{i+1}\t{self.level}\t{ev.regnum}\t\t{ev.charge}\n"
        return output

    def getRegNumFromColor(self, color, is_ev):
        collection = self.evSlots if is_ev else self.slots
        return [str(v.regnum) for v in collection if v is not None and v.color == color]
            
    def getSlotNumFromRegNum(self, regnum, is_ev):
        collection = self.evSlots if is_ev else self.slots
        for i, v in enumerate(collection):
            if v is not None and str(v.regnum) == str(regnum):
                return i + 1
        return -1
            
    def getSlotNumFromColor(self, color, is_ev): 
        collection = self.evSlots if is_ev else self.slots
        return [str(i + 1) for i, v in enumerate(collection) if v is not None and v.color == color]


class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("650x850")
        self.root.resizable(0,0)
        self.root.title("Parking Lot Manager")
        self.parkinglot = ParkingLot()

        # Variables encapsulated in the class instead of global scope
        self.num_value = tk.StringVar()
        self.ev_value = tk.StringVar()
        self.make_value = tk.StringVar()
        self.model_value = tk.StringVar()
        self.color_value = tk.StringVar()
        self.reg_value = tk.StringVar()
        self.level_value = tk.StringVar(value="1")
        self.ev_car_value = tk.IntVar()
        self.ev_motor_value = tk.IntVar()
        self.slot1_value = tk.StringVar()
        self.slot2_value = tk.StringVar()
        self.reg1_value = tk.StringVar()
        self.slot_value = tk.StringVar()
        self.ev_car2_value = tk.IntVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text='Parking Lot Manager', font='Arial 14 bold').grid(row=0, column=0, padx=10, columnspan=4)
        tk.Label(self.root, text='Lot Creation', font='Arial 12 bold').grid(row=1, column=0, padx=10, columnspan=4)

        tk.Label(self.root, text='Number of Regular Spaces', font='Arial 12').grid(row=2, column=0, padx=5)
        tk.Entry(self.root, textvariable=self.num_value, width=6, font='Arial 12').grid(row=2, column=1, padx=4, pady=2)

        tk.Label(self.root, text='Number of EV Spaces', font='Arial 12').grid(row=2, column=2, padx=5)
        tk.Entry(self.root, textvariable=self.ev_value, width=6, font='Arial 12').grid(row=2, column=3, padx=4, pady=4)

        tk.Label(self.root, text='Floor Level', font='Arial 12').grid(row=3, column=0, padx=5)
        tk.Entry(self.root, textvariable=self.level_value, width=6, font='Arial 12').grid(row=3, column=1, padx=4, pady=4)

        tk.Button(self.root, command=self.makeLot, text="Create Parking Lot", font="Arial 12", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5).grid(row=4, column=0, padx=4, pady=4)

        tk.Label(self.root, text='Car Management', font='Arial 12 bold').grid(row=5, column=0, padx=10, columnspan=4)

        tk.Label(self.root, text='Make', font='Arial 12').grid(row=6, column=0, padx=5)
        tk.Entry(self.root, textvariable=self.make_value, width=12, font='Arial 12').grid(row=6, column=1, padx=4, pady=4)

        tk.Label(self.root, text='Model', font='Arial 12').grid(row=6, column=2, padx=5)
        tk.Entry(self.root, textvariable=self.model_value, width=12, font='Arial 12').grid(row=6, column=3, padx=4, pady=4)

        tk.Label(self.root, text='Color', font='Arial 12').grid(row=7, column=0, padx=5)
        tk.Entry(self.root, textvariable=self.color_value, width=12, font='Arial 12').grid(row=7, column=1, padx=4, pady=4)

        tk.Label(self.root, text='Registration #', font='Arial 12').grid(row=7, column=2, padx=5)
        tk.Entry(self.root, textvariable=self.reg_value, width=12, font='Arial 12').grid(row=7, column=3, padx=4, pady=4)

        tk.Checkbutton(self.root, text='Electric', variable=self.ev_car_value, onvalue=1, offvalue=0, font='Arial 12').grid(column=0, row=8, padx=4, pady=4)
        tk.Checkbutton(self.root, text='Motorcycle', variable=self.ev_motor_value, onvalue=1, offvalue=0, font='Arial 12').grid(column=1, row=8, padx=4, pady=4)

        tk.Button(self.root, command=self.parkCar, text="Park Car", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5).grid(column=0, row=9, padx=4, pady=4)

        tk.Label(self.root, text='Slot #', font='Arial 12').grid(row=10, column=0, padx=5)
        tk.Entry(self.root, textvariable=self.slot_value, width=12, font='Arial 12').grid(row=10, column=1, padx=4, pady=4)

        tk.Checkbutton(self.root, text='Remove EV?', variable=self.ev_car2_value, onvalue=1, offvalue=0, font='Arial 12').grid(column=2, row=10, padx=4, pady=4)

        tk.Button(self.root, command=self.removeCar, text="Remove Car", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5).grid(column=0, row=11, padx=4, pady=4)

        tk.Label(self.root, text="").grid(row=12, column=0)

        tk.Button(self.root, command=self.slotNumByReg, text="Get Slot ID by Registration #", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5).grid(column=0, row=13, padx=4, pady=4)
        tk.Entry(self.root, textvariable=self.slot1_value, width=12, font='Arial 12').grid(row=13, column=1, padx=4, pady=4)

        tk.Button(self.root, command=self.slotNumByColor, text="Get Slot ID by Color", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5).grid(column=2, row=13, padx=4, pady=4)
        tk.Entry(self.root, textvariable=self.slot2_value, width=12, font='Arial 12').grid(row=13, column=3, padx=4, pady=4)

        tk.Button(self.root, command=self.regNumByColor, text="Get Registration # by Color", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5).grid(column=0, row=14, padx=4, pady=4)
        tk.Entry(self.root, textvariable=self.reg1_value, width=12, font='Arial 12').grid(row=14, column=1, padx=4, pady=4)

        tk.Button(self.root, command=self.chargeStatus, text="EV Charge Status", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5).grid(column=2, row=14, padx=4, pady=4)

        tk.Button(self.root, command=self.status, text="Current Lot Status", font="Arial 11", bg='PaleGreen1', fg='black', activebackground="PaleGreen3", padx=5, pady=5).grid(column=0, row=15, padx=4, pady=4)

        self.tfield = tk.Text(self.root, width=70, height=15)
        self.tfield.grid(column=0, row=16, padx=10, pady=10, columnspan=4)

    def write_output(self, text):
        self.tfield.insert(tk.INSERT, text)

    def makeLot(self):
        try:
            capacity = int(self.num_value.get())
            ev_cap = int(self.ev_value.get())
            level = int(self.level_value.get())
            self.parkinglot.createParkingLot(capacity, ev_cap, level)
            self.write_output(f"Created a parking lot with {capacity} regular slots and {ev_cap} ev slots on level: {level}\n")
        except ValueError:
            self.write_output("Error: Please enter valid integers for lot creation.\n")

    def parkCar(self):
        res = self.parkinglot.park(
            self.reg_value.get(), self.make_value.get(), self.model_value.get(), 
            self.color_value.get(), self.ev_car_value.get(), self.ev_motor_value.get()
        )
        if res == -1:
            self.write_output("Sorry, parking lot is full\n")
        else:
            self.write_output(f"Allocated slot number: {res}\n")

    def removeCar(self):
        try:
            slot = int(self.slot_value.get())
            status = self.parkinglot.leave(slot, self.ev_car2_value.get())
            if status:
                self.write_output(f"Slot number {slot} is free\n")
            else:
                self.write_output(f"Unable to remove a car from slot: {slot}\n")
        except ValueError:
            self.write_output("Error: Please enter a valid slot number.\n")

    def slotNumByReg(self):
        slot_val = self.slot1_value.get()
        slotnum = self.parkinglot.getSlotNumFromRegNum(slot_val, False)
        slotnum2 = self.parkinglot.getSlotNumFromRegNum(slot_val, True)
        
        if slotnum != -1:
            self.write_output(f"Identified slot: {slotnum}\n")
        elif slotnum2 != -1:
            self.write_output(f"Identified slot (EV): {slotnum2}\n")
        else:
            self.write_output("Not found\n")

    def slotNumByColor(self):
        color = self.slot2_value.get()
        slotnums = self.parkinglot.getSlotNumFromColor(color, False)
        slotnums2 = self.parkinglot.getSlotNumFromColor(color, True)
        if slotnums:
            self.write_output(f"Identified slots: {', '.join(slotnums)}\n")
        if slotnums2:
            self.write_output(f"Identified slots (EV): {', '.join(slotnums2)}\n")

    def regNumByColor(self):
        color = self.reg1_value.get()
        regnums = self.parkinglot.getRegNumFromColor(color, False)
        regnums2 = self.parkinglot.getRegNumFromColor(color, True)
        if regnums:
            self.write_output(f"Registation Numbers: {', '.join(regnums)}\n")
        if regnums2:
            self.write_output(f"Registation Numbers (EV): {', '.join(regnums2)}\n")

    def chargeStatus(self):
        self.write_output(self.parkinglot.chargeStatus())

    def status(self):
        self.write_output(self.parkinglot.status())


def main():
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
