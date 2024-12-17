from dataclasses import dataclass, field


@dataclass
class Computer:
    A: int
    B: int
    C: int

    program: list[int]
    pc: int = 0
    outputs: list[int] = field(default_factory=list)

    def val(self, combo: int) -> int:
        match combo:
            case 0 | 1 | 2 | 3:
                return combo
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C
            case _:
                raise ValueError

    # returns False iff it halts
    def run_inst(self) -> bool:
        if self.pc + 1 >= len(self.program):
            return False
        else:
            operand = self.program[self.pc + 1]
            jumped = False

            match self.program[self.pc]:
                case 0:
                    self.A = self.A // (2 ** self.val(operand))
                case 1:
                    self.B = self.B ^ operand
                case 2:
                    self.B = self.val(operand) % 8
                case 3:
                    if self.A != 0:
                        self.pc = operand
                        jumped = True
                case 4:
                    self.B = self.B ^ self.C
                case 5:
                    self.outputs.append(self.val(operand) % 8)
                case 6:
                    self.B = self.A // (2 ** self.val(operand))
                case 7:
                    self.C = self.A // (2 ** self.val(operand))
                case _:
                    raise ValueError

            if not jumped:
                self.pc += 2

            return True


@dataclass
class Inp:
    computer: Computer


@dataclass
class Outp:
    ans: str


def get_input() -> Inp:
    with open("in.txt", "r") as f:
        A = int(f.readline().strip().split()[-1])
        B = int(f.readline().strip().split()[-1])
        C = int(f.readline().strip().split()[-1])

        f.readline()

        program = [*map(int, f.readline().strip().split()[-1].split(","))]

        computer = Computer(A, B, C, program)

        return Inp(computer)


def solve(inp: Inp) -> Outp:
    while True:
        if not inp.computer.run_inst():
            break
    return Outp(",".join(map(str, inp.computer.outputs)))


def show_output(outp: Outp) -> None:
    print(outp.ans)


def main():
    show_output(solve(get_input()))


main()
