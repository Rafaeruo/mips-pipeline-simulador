from Instrucao import Instrucao

opcodes = ['ADD', 'ADDI', 'SUB', 'SUBI', 'BEQ', 'J', 'NOOP']

def ler_instrucoes(programa):
    instrucoes = []
    labels = {}
    variaveis = {}

    for j in range(len(programa)):    
        linha = programa[j]
        partes = linha.split(' ')

        label = ''
        opcode = ''
        i = 0
        while i < len(partes) - 1 and partes[i] == '':
            i += 1

        partes[i] = partes[i].strip('\n').upper()
        if partes[i] not in opcodes:
            label = partes[i]
            i += 1
        
        opcode = partes[i].strip('\n').upper()
        op1 = partes[i + 1].strip('\n').upper() if len(partes) > i + 1 else 0
        op2 = partes[i + 2].strip('\n').upper() if len(partes) > i + 2 else 0
        op3 = partes[i + 3].strip('\n').upper() if len(partes) > i + 3 else 0

        instrucao = Instrucao(label, opcode, op1, op2, op3, temp1=0, temp2=0, temp3=0, valida=False)
        instrucoes.append(instrucao)

        if label != '':
            labels[label] = j
            
            if opcode == '.FILL':
                variaveis[label] = int(op1)
    
    return instrucoes, labels, variaveis

def decodificar_numero_registrador(string_registrador):
    return int(string_registrador.strip(' ').strip('R'))

class Pipeline:
    def __init__(self, programa, registradores):
        self.instrucoes, self.labels, self.variaveis = ler_instrucoes(programa)
        self.pc = 0
        self.registradores = registradores
        
        self.instrucao_write_back = None
        self.instrucao_memory = None
        self.instrucao_execute = None
        self.instrucao_decode = None
        self.instrucao_fetch = None

    def write_back(self):
        if self.instrucao_execute is None:
            return
        
        opcodes_com_resultado = ['ADD', 'ADDI', 'SUB', 'SUBI']
        if self.instrucao_execute.opcode in opcodes_com_resultado:
            r0 = self.instrucao_execute.op1
            resultado = self.instrucao_execute.temp1
            self.registradores[r0] = resultado

    def memory(self):
        if self.instrucao_execute is None:
            self.instrucao_memory = None    
        else:
            self.instrucao_memory = self.instrucao_execute.clonar()

    def execute(self):
        if self.instrucao_decode is None:
            self.instrucao_execute = None
        elif self.instrucao_decode.opcode == 'NOOP':
            self.instrucao_execute = self.instrucao_decode.clonar()
        elif self.instrucao_decode.opcode == 'ADD':
            r1 = self.instrucao_decode.op2
            r2 = self.instrucao_decode.op3

            self.instrucao_execute = self.instrucao_decode.clonar()
            self.instrucao_execute.temp1 = self.registradores[r1] + self.registradores[r2]
        elif self.instrucao_decode.opcode == 'ADDI':
            r1 = self.instrucao_decode.op2
            imediato = self.instrucao_decode.op3
            valor_imediato = self.variaveis[imediato]

            self.instrucao_execute = self.instrucao_decode.clonar()
            self.instrucao_execute.temp1 = self.registradores[r1] + valor_imediato
        elif self.instrucao_decode.opcode == 'SUB':
            r1 = self.instrucao_decode.op2
            r2 = self.instrucao_decode.op3

            self.instrucao_execute = self.instrucao_decode.clonar()
            self.instrucao_execute.temp1 = self.registradores[r1] - self.registradores[r2]
        elif self.instrucao_decode.opcode == 'SUBI':
            r1 = self.instrucao_decode.op2
            imediato = self.instrucao_decode.op3
            valor_imediato = self.variaveis[imediato]

            self.instrucao_execute = self.instrucao_decode.clonar()
            self.instrucao_execute.temp1 = self.registradores[r1] - valor_imediato
        elif self.instrucao_decode.opcode == 'BEQ':
            r0 = self.instrucao_decode.op1
            r1 = self.instrucao_decode.op2
            label = self.instrucao_decode.op3

            if self.registradores[r0] == self.registradores[r1]:
                self.pc = self.labels[label]
        elif self.instrucao_decode.opcode == 'J':
            label = self.instrucao_decode.op1
            self.pc = self.labels[label]

    def decode(self):
        if self.instrucao_fetch is None:
            self.instrucao_decode = None
        elif self.instrucao_fetch.opcode == 'NOOP' or self.instrucao_fetch.opcode == 'J':
            self.instrucao_decode = self.instrucao_fetch.clonar()
        elif self.instrucao_fetch.opcode == 'ADD' or self.instrucao_fetch.opcode == 'SUB':
            self.instrucao_decode = self.instrucao_fetch.clonar()
            self.instrucao_decode.op1 = decodificar_numero_registrador(self.instrucao_decode.op1)
            self.instrucao_decode.op2 = decodificar_numero_registrador(self.instrucao_decode.op2)
            self.instrucao_decode.op3 = decodificar_numero_registrador(self.instrucao_decode.op3)
        elif self.instrucao_fetch.opcode == 'ADDI' or self.instrucao_fetch.opcode == 'SUBI' or self.instrucao_fetch.opcode == 'BEQ':
            self.instrucao_decode = self.instrucao_fetch.clonar()
            self.instrucao_decode.op1 = decodificar_numero_registrador(self.instrucao_decode.op1)
            self.instrucao_decode.op2 = decodificar_numero_registrador(self.instrucao_decode.op2)

    def fetch(self):
        if self.pc >= len(self.instrucoes):
            self.instrucao_fetch = None
        else:
            self.instrucao_fetch = self.instrucoes[self.pc]

    def run(self):
        while self.pc < len(self.instrucoes):
            self.write_back()
            self.memory()
            self.execute()
            self.decode()
            self.fetch()
            self.pc += 1
            print(self.registradores)
