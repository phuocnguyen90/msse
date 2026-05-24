import tkinter as tk
import random
import string
from ParkingManager import ParkingLot


class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x800")
        self.root.resizable(0, 0)
        self.root.title("Parking Lot Manager — Design Patterns Demonstration")

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

        self._setup_layout()
        self.create_widgets()

        ParkingLot.set_trace_callback(self._append_trace)
        self.parkinglot = ParkingLot()

    def _setup_layout(self):
        tk.Label(self.root, text="Parking Lot Manager — Live Logic Trace Demonstration",
                 font="Arial 16 bold", fg="darkblue").pack(pady=8)

        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.left_frame = tk.Frame(main_frame, width=600, relief=tk.RIDGE, bd=2)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.left_frame.pack_propagate(False)

        self.right_frame = tk.Frame(main_frame, width=500, relief=tk.RIDGE, bd=2)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        self.right_frame.pack_propagate(False)

        tk.Label(self.right_frame, text="Logic Trace Console",
                 font="Arial 12 bold", fg="darkgreen").pack(anchor="nw", padx=5, pady=5)
        self.trace_field = tk.Text(self.right_frame, width=60, height=20, bg="black", fg="lightgreen",
                                   font=("Courier New", 9), state=tk.DISABLED)
        self.trace_field.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.bottom_frame = tk.Frame(self.root, relief=tk.RIDGE, bd=2)
        self.bottom_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(self.bottom_frame, text="Application Output / Results",
                 font="Arial 12 bold", fg="darkblue").pack(anchor="nw", padx=5, pady=5)
        self.tfield = tk.Text(self.bottom_frame, width=130, height=12, font=("Courier New", 10))
        self.tfield.pack(fill=tk.X, expand=True, padx=5, pady=5)

    def _append_trace(self, message):
        self.trace_field.config(state=tk.NORMAL)
        self.trace_field.insert(tk.END, message + "\n")
        self.trace_field.see(tk.END)
        self.trace_field.config(state=tk.DISABLED)

    def create_widgets(self):
        tk.Label(self.left_frame, text="Lot Creation", font="Arial 12 bold",
                 fg="darkblue").grid(row=0, column=0, padx=10, pady=5, columnspan=4, sticky="w")

        tk.Label(self.left_frame, text="Regular Spaces", font="Arial 11").grid(row=1, column=0, padx=5, sticky="e")
        tk.Entry(self.left_frame, textvariable=self.num_value, width=6, font="Arial 11").grid(row=1, column=1, padx=4, pady=2, sticky="w")

        tk.Label(self.left_frame, text="EV Spaces", font="Arial 11").grid(row=1, column=2, padx=5, sticky="e")
        tk.Entry(self.left_frame, textvariable=self.ev_value, width=6, font="Arial 11").grid(row=1, column=3, padx=4, pady=2, sticky="w")

        tk.Label(self.left_frame, text="Floor Level", font="Arial 11").grid(row=2, column=0, padx=5, sticky="e")
        tk.Entry(self.left_frame, textvariable=self.level_value, width=6, font="Arial 11").grid(row=2, column=1, padx=4, pady=2, sticky="w")

        tk.Button(self.left_frame, command=self.makeLot, text="Create Parking Lot", font="Arial 11",
                  bg="lightblue", fg="black", activebackground="teal", padx=5, pady=5).grid(
                      row=3, column=0, padx=4, pady=6, columnspan=4)

        tk.Label(self.left_frame, text="Vehicle Management", font="Arial 12 bold",
                 fg="darkblue").grid(row=4, column=0, padx=10, pady=5, columnspan=4, sticky="w")

        tk.Label(self.left_frame, text="Make", font="Arial 11").grid(row=5, column=0, padx=5, sticky="e")
        tk.Entry(self.left_frame, textvariable=self.make_value, width=12, font="Arial 11").grid(row=5, column=1, padx=4, pady=2, sticky="w")

        tk.Label(self.left_frame, text="Model", font="Arial 11").grid(row=5, column=2, padx=5, sticky="e")
        tk.Entry(self.left_frame, textvariable=self.model_value, width=12, font="Arial 11").grid(row=5, column=3, padx=4, pady=2, sticky="w")

        tk.Label(self.left_frame, text="Color", font="Arial 11").grid(row=6, column=0, padx=5, sticky="e")
        tk.Entry(self.left_frame, textvariable=self.color_value, width=12, font="Arial 11").grid(row=6, column=1, padx=4, pady=2, sticky="w")

        tk.Label(self.left_frame, text="Registration #", font="Arial 11").grid(row=6, column=2, padx=5, sticky="e")
        tk.Entry(self.left_frame, textvariable=self.reg_value, width=12, font="Arial 11").grid(row=6, column=3, padx=4, pady=2, sticky="w")

        tk.Checkbutton(self.left_frame, text="Electric Vehicle", variable=self.ev_car_value,
                       onvalue=1, offvalue=0, font="Arial 11").grid(row=7, column=0, padx=4, pady=4, sticky="w")
        tk.Checkbutton(self.left_frame, text="Motorcycle", variable=self.ev_motor_value,
                       onvalue=1, offvalue=0, font="Arial 11").grid(row=7, column=1, padx=4, pady=4, sticky="w")

        tk.Button(self.left_frame, command=self.parkCar, text="Park Vehicle", font="Arial 11",
                  bg="lightblue", fg="black", activebackground="teal", padx=5, pady=5).grid(
                      row=8, column=0, padx=4, pady=6, columnspan=2, sticky="ew")

        tk.Button(self.left_frame, command=self.randomizeVehicle, text="Randomize", font="Arial 11",
                  bg="lightyellow", fg="black", activebackground="orange", padx=5, pady=5).grid(
                      row=8, column=2, padx=4, pady=6, columnspan=2, sticky="ew")

        tk.Label(self.left_frame, text="Remove Vehicle", font="Arial 12 bold",
                 fg="darkblue").grid(row=9, column=0, padx=10, pady=5, columnspan=4, sticky="w")

        tk.Label(self.left_frame, text="Slot #", font="Arial 11").grid(row=10, column=0, padx=5, sticky="e")
        tk.Entry(self.left_frame, textvariable=self.slot_value, width=12, font="Arial 11").grid(row=10, column=1, padx=4, pady=2, sticky="w")

        tk.Checkbutton(self.left_frame, text="Remove EV?", variable=self.ev_car2_value,
                       onvalue=1, offvalue=0, font="Arial 11").grid(row=10, column=2, padx=4, pady=4, sticky="w")

        tk.Button(self.left_frame, command=self.removeCar, text="Remove Vehicle", font="Arial 11",
                  bg="lightblue", fg="black", activebackground="teal", padx=5, pady=5).grid(
                      row=11, column=0, padx=4, pady=6, columnspan=4)

        tk.Label(self.left_frame, text="Queries", font="Arial 12 bold",
                 fg="darkblue").grid(row=12, column=0, padx=10, pady=5, columnspan=4, sticky="w")

        tk.Button(self.left_frame, command=self.slotNumByReg, text="Slot by Reg #", font="Arial 11",
                  bg="lightblue", fg="black", activebackground="teal", padx=5, pady=5).grid(row=13, column=0, padx=4, pady=4)
        tk.Entry(self.left_frame, textvariable=self.slot1_value, width=12, font="Arial 11").grid(row=13, column=1, padx=4, pady=4, sticky="w")

        tk.Button(self.left_frame, command=self.slotNumByColor, text="Slot by Color", font="Arial 11",
                  bg="lightblue", fg="black", activebackground="teal", padx=5, pady=5).grid(row=13, column=2, padx=4, pady=4)
        tk.Entry(self.left_frame, textvariable=self.slot2_value, width=12, font="Arial 11").grid(row=13, column=3, padx=4, pady=4, sticky="w")

        tk.Button(self.left_frame, command=self.regNumByColor, text="Reg # by Color", font="Arial 11",
                  bg="lightblue", fg="black", activebackground="teal", padx=5, pady=5).grid(row=14, column=0, padx=4, pady=4)
        tk.Entry(self.left_frame, textvariable=self.reg1_value, width=12, font="Arial 11").grid(row=14, column=1, padx=4, pady=4, sticky="w")

        tk.Button(self.left_frame, command=self.chargeStatus, text="EV Charge Status", font="Arial 11",
                  bg="lightblue", fg="black", activebackground="teal", padx=5, pady=5).grid(row=14, column=2, padx=4, pady=4)

        tk.Button(self.left_frame, command=self.status, text="Current Lot Status", font="Arial 11",
                  bg="PaleGreen1", fg="black", activebackground="PaleGreen3", padx=5, pady=5).grid(row=15, column=0, padx=4, pady=6, columnspan=4)

    def write_output(self, text):
        self.tfield.insert(tk.INSERT, text + "\n")
        self.tfield.see(tk.END)

    def makeLot(self):
        try:
            capacity = int(self.num_value.get())
            ev_cap = int(self.ev_value.get())
            level = int(self.level_value.get())
            self.parkinglot.createParkingLot(capacity, ev_cap, level)
            self.write_output(f"Created a parking lot with {capacity} regular slots and {ev_cap} EV slots on level: {level}\n")
        except ValueError as e:
            msg = str(e)
            if "invalid literal" in msg:
                self.write_output("Error: Please enter valid integers for lot creation.\n")
            else:
                self.write_output(f"Error: {msg}\n")

    def parkCar(self):
        try:
            res = self.parkinglot.park(
                self.reg_value.get(), self.make_value.get(), self.model_value.get(),
                self.color_value.get(), self.ev_car_value.get(), self.ev_motor_value.get()
            )
            if res == -1:
                self.write_output("Sorry, parking lot is full\n")
            else:
                self.write_output(f"Allocated slot number: {res}\n")
        except ValueError as e:
            self.write_output(f"Error: {str(e)}\n")

    def randomizeVehicle(self):
        makes = ["Toyota", "Honda", "Ford", "Tesla", "Nissan", "Chevrolet", "BMW", "Audi", "Yamaha", "Zero"]
        models = ["Civic", "Corolla", "Mustang", "Model S", "Leaf", "Volt", "X5", "A4", "R1", "SR/F"]
        colors = ["Red", "Blue", "Black", "White", "Silver", "Green"]
        
        self.make_value.set(random.choice(makes))
        self.model_value.set(random.choice(models))
        self.color_value.set(random.choice(colors))
        self.reg_value.set("".join(random.choices(string.ascii_uppercase + string.digits, k=6)))
        self.ev_car_value.set(random.choice([0, 1]))
        self.ev_motor_value.set(random.choice([0, 1]))

    def removeCar(self):
        try:
            slot = int(self.slot_value.get())
            status = self.parkinglot.leave(slot, self.ev_car2_value.get())
            if status:
                self.write_output(f"Slot number {slot} is free\n")
            else:
                self.write_output(f"Unable to remove a vehicle from slot: {slot}\n")
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
            self.write_output(f"Registration Numbers: {', '.join(regnums)}\n")
        if regnums2:
            self.write_output(f"Registration Numbers (EV): {', '.join(regnums2)}\n")

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
