import sys
import argparse
from jvm_creator import JVM_Creator, load_ins, TreeVisitorJVM
from llvm_creator import LLVM_Creator
from lark import Lark, Tree, Token
from grammar import instant_grammar



if __name__ == "__main__":
    creator = JVM_Creator()
    parser = Lark(instant_grammar, start="program")

    arg_parser = argparse.ArgumentParser(description="Instant to LLVM IR compiler")
    arg_parser.add_argument('input_file', help='Ścieżka do pliku wejściowego .ins')
    arg_parser.add_argument('-o', '--output', help='Ścieżka do pliku wyjściowego .ll', required=True)

    args = arg_parser.parse_args()
    file_name = args.output
    visitor = TreeVisitorJVM()

    program = load_ins(args.input_file)

    tree = parser.parse(program)
    visitor.visit(tree)
    instructions= visitor.get_instructions()
    stack_limit = visitor.stack_limit
    variable_limit = visitor.locals_limit

    creator.create_jvm(file_name, stack_limit, variable_limit, instructions)
