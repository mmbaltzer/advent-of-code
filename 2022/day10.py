# Devices are components of the handheld that rely on the Clock to advance
class Device:
    def __init__(self) -> None:
        pass
    def advance_cycle():
        pass

class CpuBoi(Device):
    def __init__(self) -> None:
        self.busy = 0
        self.x = 1
        self.v = 0
        self.instruction = None

    def addv(self):
        self.x += self.v
        self.v = 0

    def noop(self):
        pass
    
    def advance_cycle(self):
        self.busy -= 1
        if self.busy == 0:
            self.finish_instruction()
    
    def finish_instruction(self):
        self.instruction()
        self.instruction = None

    def send_instruction(self, instruction_string):
        if instruction_string[0:4] == 'noop':
            self.busy = 1
            self.instruction = self.noop
        else:
            self.busy = 2
            self.v = int(instruction_string.split()[1])
            self.instruction = self.addv

class CathodeBoi(Device):
    def __init__(self) -> None:
        self.curr_pixel = 0
        self.n_rows = 6
        self.n_cols = 40
        self.n_pixels = self.n_rows * self.n_cols
        self.image = ""
    
    def advance_cycle(self):
        self.curr_pixel += 1
        if self.curr_pixel >= self.n_pixels - 1:
            self.curr_pixel = 0

    def draw_pixel(self, cpu_register):
        if abs(self.curr_pixel % self.n_cols - cpu_register) <= 1:
            self.image = self.image + "#"
        else:
            self.image = self.image + "."
    
    def draw_image(self):
        rows = [[i*self.n_cols, (i+1)*self.n_cols] for i in range(self.n_rows)]
        [print(self.image[r[0]:r[1]]) for r in rows]
    
    # debugging helper
    def draw_current_row(self):
        start = (self.curr_pixel // self.n_cols) * self.n_cols
        print(self.image[start:])

class ClockBoi:
    def __init__(self, devices=[]) -> None:
        self.cycle = 1
        self.devices_list = devices
    
    def add_device(self, device):
        self.devices_list.append(device)

    def advance_clock(self):
        self.cycle += 1
        for d in self.devices_list:
            d.advance_cycle()

def send_instructions_tracking_signal(clock, cpu, instructions, cycles):
    # initialize components
    clock.add_device(cpu)

    # tracking variables for signals
    tracked_signal = [None for _ in cycles]
    looking_for = 0

    # simulate handheld device
    while clock.cycle <= max(cycles):
        if not cpu.busy:
            cpu.send_instruction(instructions.pop(0))
        
        if clock.cycle == cycles[looking_for]:
            tracked_signal[looking_for] = cpu.x * clock.cycle
            looking_for += 1

        clock.advance_clock()

    return tracked_signal

def send_instructions_drawing_image(clock, cpu, cathode, instructions) -> None:
    # initialize components
    clock.add_device(cpu)
    clock.add_device(cathode)
    
    # simulate handheld device
    while clock.cycle <= cathode.n_pixels:
        if not cpu.busy:
            cpu.send_instruction(instructions.pop(0))
        cathode.draw_pixel(cpu.x)
        clock.advance_clock()

    cathode.draw_image()
    return

# debugging helper
def draw_sprite(cathode_width, cpu_register):
    return "." * (cpu_register-2) + "###" + "." * (cathode_width - (cpu_register + 1))

def parta():
    instruction_lines = open('2022/data/day10.txt', 'r').read().split('\n')
    cycles = [20, 60, 100, 140, 180, 220]
    tracked_signal = send_instructions_tracking_signal(ClockBoi(), CpuBoi(), instruction_lines, cycles)
    print( tracked_signal )
    print( sum(tracked_signal) )

def partb():
    instruction_lines = open('2022/data/day10.txt', 'r').read().split('\n')
    send_instructions_drawing_image(ClockBoi(), CpuBoi(), CathodeBoi(), instruction_lines)

parta()
partb()