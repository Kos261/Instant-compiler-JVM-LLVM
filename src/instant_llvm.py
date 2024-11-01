import sys
import argparse
from llvm_creator import LLVM_Creator, TreeVisitorLLVM, load_ins
from lark import Lark, Tree, Token
from grammar import instant_grammar


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Instant to LLVM IR compiler")
    parser.add_argument('input_file', help='Ścieżka do pliku wejściowego .ins')
    parser.add_argument('-o', '--output', help='Ścieżka do pliku wyjściowego .ll', required=True)
    args = parser.parse_args()

    program = load_ins(args.input_file)

    visitor = TreeVisitorLLVM()
    tree = Lark(instant_grammar, start="program").parse(program)
    visitor.visit(tree)
    instructions, last_register = visitor.get_instructions()

    # Zapisz kod LLVM do pliku wyjściowego
    creator = LLVM_Creator()
    creator.create_llvm(instructions, last_register, filename=args.output)