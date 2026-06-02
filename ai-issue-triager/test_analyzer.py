from tools.file_tools import read_repository_file
from tools.analyzer import analyze_syntax_complexity


content = read_repository_file("src/billing.py")

result = analyze_syntax_complexity(content)

print(result)