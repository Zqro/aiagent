from functions.get_files_info import get_files_info

print(get_files_info("calculator", "main.py"))
print(get_files_info("calculator", "pkg/calculator.py"))
print(get_files_info("calculator", "/bin/cat"))
print(get_files_info("calculator", "pkg/does_not_exist.py"))
