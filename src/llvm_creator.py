from lark import Lark, Tree, Token
import os


class TreeVisitorLLVM:
    def __init__(self) -> None:
        self.instructions = []
        self.variable_index = {}
        self.counter = 0
        self.last_register = None
        self.printable_registers = [] 

    def visit(self, node):
        if isinstance(node, Tree):
            method_name = f"visit_{node.data}"
            visitor = getattr(self, method_name, self.default_visit)
            return visitor(node)
        elif isinstance(node, Token):
            return node.value
        return None
    
    def default_visit(self, node):
        results = []
        for child in node.children:
            result = self.visit(child)
            if result is not None:
                results.append(result)
        if results:
            return results[-1]
        return None


    def visit_prog(self, node):
        for stmt in node.children:
            self.visit(stmt)

    def visit_expression_stmt(self, node):
        result_register = self.visit(node.children[0])
        if result_register:
            self.printable_registers.append(result_register)

    def visit_term_expr(self, node):
        return self.visit(node.children[0])

    def visit_factor_expr(self, node):
        return self.visit(node.children[0])

    def visit_exp_paren(self, node):
        return self.visit(node.children[0])

    def visit_exp_sub(self, node):
        return self.instructions_add_sub_mul_div(node, "sub")
        
    def visit_exp_add(self, node):
        return self.instructions_add_sub_mul_div(node, "add")

    def visit_exp_mul(self, node):
        return self.instructions_add_sub_mul_div(node, "mul")
    
    def visit_exp_div(self, node):
        return self.instructions_add_sub_mul_div(node, "sdiv")

    def visit_exp_lit(self, node):
        value = self.visit(node.children[0])
        reg = f"%result_{self.counter}"
        self.counter += 1
        self.instructions.append(f"{reg} = add i32 0, {value}")
        self.last_register = reg
        return reg
   
    def visit_exp_var(self, node):
        var_name = self.visit(node.children[0])  
        if var_name not in self.variable_index:
            self.instructions.append(f"%{var_name} = alloca i32")
            self.variable_index[var_name] = True
            self.instructions.append(f"store i32 0, i32* %{var_name}")

        reg = f"%result_{self.counter}"
        self.counter += 1
        self.instructions.append(f"{reg} = load i32, i32* %{var_name}")
        return reg

    def instructions_add_sub_mul_div(self, node, operator):
        left_reg = self.visit(node.children[0])
        right_reg = self.visit(node.children[1])

        result_reg = f"%result_{self.counter}"
        self.counter += 1

        self.instructions.append(f"{result_reg} = {operator} i32 {left_reg}, {right_reg}")
        self.last_register = result_reg
        return result_reg

    def visit_assignment(self, node):
        var_name = self.visit(node.children[0])  
        value_reg = self.visit(node.children[1])

        if var_name not in self.variable_index:
            self.instructions.append(f"%{var_name} = alloca i32")
            self.variable_index[var_name] = True

        self.instructions.append(f"store i32 {value_reg}, i32* %{var_name}")

    def get_instructions(self):
        return self.instructions, self.printable_registers


class LLVM_Creator:
    def __init__(self):
        self.printf_decl = 'declare i32 @printf(i8*, ...)\n'
        self.format_str = '@format_str = constant [4 x i8] c"%d\\0A\\00"\n'

        self.start_part = """
define i32 @main() {
entry:
"""

    def create_llvm(self, instructions, printable_registers, filename="TEST"):
        base_filename = os.path.splitext(os.path.basename(filename))[0]
        os.makedirs('foo/bar', exist_ok=True)

        with open(f"foo/bar/{base_filename}.ll", mode='w') as file:
            file.write(self.printf_decl)
            file.write(self.format_str)
            file.write(self.start_part)

            for instruction in instructions:
                file.write(instruction + "\n")
            
            for i, reg in enumerate(printable_registers):
                file.write(f"%fmt_ptr{i} = getelementptr [4 x i8], [4 x i8]* @format_str, i32 0, i32 0\n")
                file.write(f"call i32 (i8*, ...) @printf(i8* %fmt_ptr{i}, i32 {reg})\n")
            
            file.write("ret i32 0\n")
            file.write("}\n")


def load_ins(filepath):
    program = ""
    with open(filepath, mode='r') as f:
        program = "".join(line.strip() for line in f)
    return program
