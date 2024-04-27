class Instrucao:
    def __init__(self, label, opcode, op1, op2, op3, temp1, temp2, temp3, valida):
        self.label = label
        self.opcode = opcode
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3
        self.temp1 = temp1
        self.temp2 = temp2
        self.temp3 = temp3
        self.valida = valida
    
    def clonar(self):
        return Instrucao(self.label, self.opcode, self.op1, self.op2, self.op3, self.temp1, self.temp2, self.temp3, self.valida)
        