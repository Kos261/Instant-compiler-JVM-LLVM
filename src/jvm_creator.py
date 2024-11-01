from lark import Lark, Tree, Token
import os
from pathlib import Path
cwd = Path.cwd()
Project_path = cwd.parent

class TreeVisitorJVM:
    def __init__(self) -> None:
        self.instructions = []
        self.stack_limit = 0
        self.locals_limit = 1
        self.variable_index = {}
        self.current_stack = 0

    def update_stack(self, change):
        self.current_stack += change
        if self.current_stack > self.stack_limit:
            self.stack_limit = self.current_stack
        if self.current_stack < 0:
            self.current_stack = 0 
    
    def visit(self, node):
        if isinstance(node, Tree):
            method_name = f"visit_{node.data}"
            visitor = getattr(self, method_name, self.default_visit)
            return visitor(node)
        elif isinstance(node, Token):
            return node.value
        return None
    
    def default_visit(self, node):
        for child in node.children:
            self.visit(child)

    def visit_expression_stmt(self, node):

        self.instructions.append("getstatic java/lang/System/out Ljava/io/PrintStream;")
        self.update_stack(1)

        for child in node.children:
            self.visit(child)

        self.instructions.append("invokevirtual java/io/PrintStream/println(I)V")
        self.update_stack(-2)


    def visit_exp_sub(self, node):
        left, right = node.children
        self.visit(left)
        self.visit(right)
        self.update_stack(-1)  
        self.instructions.append("isub")
        
    def visit_exp_add(self, node):
        left, right = node.children
        self.visit(left)
        self.visit(right)
        self.update_stack(-1) 
        self.instructions.append("iadd")
    
    def visit_exp_mul(self, node):
        left, right = node.children
        self.visit(left)
        self.visit(right)
        self.update_stack(-1)  
        self.instructions.append("imul")
    
    def visit_exp_div(self, node):
        left, right = node.children
        self.visit(left)
        self.visit(right)
        self.update_stack(-1)  
        self.instructions.append("idiv")

    def visit_exp_lit(self, node):
        value = int(node.children[0].value)
        node.value = value  
        self.update_stack(1)

        if 0 <= value <= 5:
            self.instructions.append(f"iconst_{value}")
        elif value == -1:
            self.instructions.append("iconst_m1")
        elif -128 <= value <= 127:
            self.instructions.append(f"bipush {value}")
        elif -32768 <= value <= 32767:
            self.instructions.append(f"sipush {value}")
        else:
            self.instructions.append(f"ldc {value}")

    def visit_exp_var(self, node):
        var_name = node.children[0].value
        
        if var_name not in self.variable_index:
            self.variable_index[var_name] = len(self.variable_index)
            self.locals_limit = max(self.locals_limit, self.variable_index[var_name] + 1)

        node.var_index = self.variable_index[var_name] 
        self.instructions.append(f"iload {node.var_index}")
        self.update_stack(1)


    def visit_assignment(self, node):
        var_name = node.children[0].value
        value_node = node.children[1]
        self.visit(value_node)

        if var_name not in self.variable_index:
            self.variable_index[var_name] = len(self.variable_index)
            self.locals_limit = max(self.locals_limit, self.variable_index[var_name] + 1)

        node.var_index = self.variable_index[var_name]

        if node.var_index <= 3:
            self.instructions.append(f"istore_{node.var_index}")
        else:
            self.instructions.append(f"istore {node.var_index}")
        self.update_stack(-1)


    def get_instructions(self):
        return self.instructions

class JVM_Creator:
    def __init__(self):
        self.start_part = ".class public {}\n.super java/lang/Object\n\n; standard initializer\n.method public <init>()V\n    aload_0\n    invokespecial java/lang/Object/<init>()V\n    return\n.end method\n\n.method public static main([Ljava/lang/String;)V\n.limit stack {}\n.limit locals {}\n"
        self.end_part = """
return
.end method
"""

    def create_jvm(self, filename, stack_limit, variable_limit, jvm_instructions):
        base_filename = os.path.splitext(os.path.basename(filename))[0]
        output_dir = os.path.dirname(filename)
        output_path = os.path.join(output_dir, f"{base_filename}.j")
    
        self.start_part = self.start_part.format(base_filename, stack_limit, variable_limit)

        with open(output_path, mode='w') as file:
            file.write(self.start_part + "\n")
            for line in jvm_instructions:
                file.write(line + "\n")
            file.write(self.end_part)


def load_ins(filepath):
    with open(filepath, mode='r') as f:
        program = "".join(line.strip() for line in f)
    return program

