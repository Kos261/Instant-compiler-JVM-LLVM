PYTHON = python3
LLVM_AS = llvm-as
CLANG = clang
JASMIN = java -jar lib/jasmin.jar

all: insc_llvm insc_jvm

insc_llvm: src/instant_llvm.py
	@echo "Tworzenie insc_llvm"
	@echo "#!/usr/bin/env bash" > insc_llvm
	@echo "" >> insc_llvm
	@echo "# Skrypt kompilatora LLVM" >> insc_llvm
	@echo "" >> insc_llvm
	@echo 'if [ "$$#" -ne 1 ]; then' >> insc_llvm
	@echo '    echo "Użycie: $$0 ścieżka/do/pliku.ins"' >> insc_llvm
	@echo '    exit 1' >> insc_llvm
	@echo 'fi' >> insc_llvm
	@echo "" >> insc_llvm
	@echo 'INPUT_FILE="$$1"' >> insc_llvm
	@echo 'INPUT_DIR="$$(dirname "$$INPUT_FILE")"' >> insc_llvm
	@echo 'INPUT_BASENAME="$$(basename "$$INPUT_FILE" .ins)"' >> insc_llvm
	@echo "" >> insc_llvm
	@echo 'OUTPUT_LL="$$INPUT_DIR/$$INPUT_BASENAME.ll"' >> insc_llvm
	@echo 'OUTPUT_BC="$$INPUT_DIR/$$INPUT_BASENAME.bc"' >> insc_llvm
	@echo "" >> insc_llvm
	@echo '$(PYTHON) src/instant_llvm.py "$$INPUT_FILE" -o "$$OUTPUT_LL"' >> insc_llvm
	@echo '$(LLVM_AS) "$$OUTPUT_LL" -o "$$OUTPUT_BC"' >> insc_llvm
	@echo 'chmod +x "$$OUTPUT_BC"' >> insc_llvm
	@echo 'echo "Uruchamianie $$OUTPUT_BC"' >> insc_llvm
	@echo './"$$OUTPUT_BC"' >> insc_llvm
	@chmod +x insc_llvm


insc_jvm: src/instant_jvm.py
	@echo "Tworzenie insc_jvm"
	@echo "#!/usr/bin/env bash" > insc_jvm
	@echo "" >> insc_jvm
	@echo "# Skrypt kompilatora JVM" >> insc_jvm
	@echo "" >> insc_jvm
	@echo 'if [ "$$#" -ne 1 ]; then' >> insc_jvm
	@echo '    echo "Użycie: $$0 ścieżka/do/pliku.ins"' >> insc_jvm
	@echo '    exit 1' >> insc_jvm
	@echo 'fi' >> insc_jvm
	@echo "" >> insc_jvm
	@echo 'INPUT_FILE="$$1"' >> insc_jvm
	@echo 'INPUT_DIR="$$(dirname "$$INPUT_FILE")"' >> insc_jvm
	@echo 'INPUT_BASENAME="$$(basename "$$INPUT_FILE" .ins)"' >> insc_jvm
	@echo "" >> insc_jvm
	@echo 'OUTPUT_J="$$INPUT_DIR/$$INPUT_BASENAME.j"' >> insc_jvm
	@echo 'OUTPUT_CLASS="$$INPUT_DIR/$$INPUT_BASENAME.class"' >> insc_jvm
	@echo 'EXECUTABLE="$$INPUT_DIR/$$INPUT_BASENAME"' >> insc_jvm
	@echo "" >> insc_jvm
	@echo 'echo "Kompilacja $$INPUT_FILE do $$OUTPUT_J"' >> insc_jvm
	@echo '$(PYTHON) src/instant_jvm.py "$$INPUT_FILE" -o "$$OUTPUT_J"' >> insc_jvm
	@echo 'echo "Kompilacja $$OUTPUT_J do $$OUTPUT_CLASS"' >> insc_jvm
	@echo '$(JASMIN) "$$OUTPUT_J" -d "$$INPUT_DIR"' >> insc_jvm
	@echo "" >> insc_jvm
	@echo 'echo "Tworzenie skryptu wykonywalnego $$EXECUTABLE"' >> insc_jvm
	@echo 'echo "#!/usr/bin/env bash" > "$$EXECUTABLE"' >> insc_jvm
	@echo 'echo "java -cp \\"$$INPUT_DIR\\" \\"$$INPUT_BASENAME\\"" >> "$$EXECUTABLE"' >> insc_jvm
	@echo 'chmod +x "$$EXECUTABLE"' >> insc_jvm
	@echo "" >> insc_jvm
	@echo 'echo "Uruchamianie $$EXECUTABLE"' >> insc_jvm
	@echo '"$$EXECUTABLE"' >> insc_jvm
	@chmod +x insc_jvm


clean:
	rm -f insc_llvm insc_jvm
