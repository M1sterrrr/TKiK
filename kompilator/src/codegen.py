from __future__ import annotations

from . import parser as ast


class CGenerator:
    def __init__(self):
        self.lines = []
        self.indent_level = 0
        self.declared_vars = set()

    def emit(self, line: str = ""):
        self.lines.append("    " * self.indent_level + line)

    def generate(self, node: ast.Program) -> str:
        self.emit("#include <stdio.h>")
        self.emit("#include <stdbool.h>")
        self.emit()
        self.emit("int main() {")
        self.indent_level += 1

        int_vars: set[str] = set()
        bool_vars: set[str] = set()

        for decl in node.declarations:
            for name in decl.names:
                if decl.vartype == "integer":
                    int_vars.add(name)
                elif decl.vartype == "boolean":
                    bool_vars.add(name)
                else:
                    raise NotImplementedError(f"Unknown var type: {decl.vartype}")

        self.declared_vars = int_vars | bool_vars

        if int_vars:
            self.emit(f"int {', '.join(sorted(int_vars))};")
        if bool_vars:
            self.emit(f"bool {', '.join(sorted(bool_vars))};")

        self.gen_stmt(node.body)

        self.emit("return 0;")
        self.indent_level -= 1
        self.emit("}")
        return "\n".join(self.lines) + "\n"

    def gen_stmt(self, node):
        if isinstance(node, ast.Compound):
            for s in node.statements:
                self.gen_stmt(s)
        elif isinstance(node, ast.Assign):
            expr = self.gen_expr(node.expr)
            self.emit(f"{node.name} = {expr};")
        elif isinstance(node, ast.Writeln):
            # integer-only for now
            for i, e in enumerate(node.exprs):
                expr = self.gen_expr(e)
                if i == 0:
                    self.emit(f'printf("%d", {expr});')
                else:
                    # separation between printed values
                    self.emit('printf(" ");')
                    self.emit(f'printf("%d", {expr});')
            self.emit('printf("\\n");')
        elif isinstance(node, ast.Readln):
            self.emit(f'scanf("%d", &{node.name});')
        elif isinstance(node, ast.If):
            cond = self.gen_expr(node.cond)
            self.emit(f"if ({cond}) {{")
            self.indent_level += 1
            self.gen_stmt(node.then_stmt)
            self.indent_level -= 1
            if node.else_stmt is not None:
                self.emit("} else {")
                self.indent_level += 1
                self.gen_stmt(node.else_stmt)
                self.indent_level -= 1
            self.emit("}")
        elif isinstance(node, ast.While):
            cond = self.gen_expr(node.cond)
            self.emit(f"while ({cond}) {{")
            self.indent_level += 1
            self.gen_stmt(node.body)
            self.indent_level -= 1
            self.emit("}")
        elif isinstance(node, ast.For):
            # if loop variable wasn't declared in var-section, declare it (int-only compiler)
            if node.var_name not in self.declared_vars:
                self.declared_vars.add(node.var_name)
                # emit declaration immediately (simple, predictable semantics)
                self.emit(f"int {node.var_name};")

            start = self.gen_expr(node.start_expr)
            end = self.gen_expr(node.end_expr)
            if node.direction == "to":
                self.emit(f"for ({node.var_name} = {start}; {node.var_name} <= {end}; {node.var_name}++) {{")
            elif node.direction == "downto":
                self.emit(f"for ({node.var_name} = {start}; {node.var_name} >= {end}; {node.var_name}--) {{")
            else:
                raise NotImplementedError(f"Unknown for direction: {node.direction}")
            self.indent_level += 1
            self.gen_stmt(node.body)
            self.indent_level -= 1
            self.emit("}")
        elif isinstance(node, ast.RepeatUntil):
            # Pascal: repeat ... until cond;  =>  do { ... } while (!(cond));
            cond = self.gen_expr(node.cond)
            self.emit("do {")
            self.indent_level += 1
            for s in node.body_statements:
                self.gen_stmt(s)
            self.indent_level -= 1
            self.emit(f"}} while (!({cond}));")
        else:
            raise NotImplementedError(f"Unknown statement node: {type(node).__name__}")

    def gen_expr(self, node) -> str:
        if isinstance(node, ast.Num):
            return str(node.value)
        if isinstance(node, ast.Bool):
            return "true" if node.value else "false"
        if isinstance(node, ast.Var):
            return node.name
        if isinstance(node, ast.UnaryOp):
            inner = self.gen_expr(node.expr)
            if node.op == "-":
                return f"(-{inner})"
            if node.op == "+":
                return f"({inner})"
            if node.op == "not":
                return f"(!({inner}))"
            raise NotImplementedError(f"Unknown unary operator: {node.op}")
        if isinstance(node, ast.BinOp):
            left = self.gen_expr(node.left)
            right = self.gen_expr(node.right)
            op = node.op
            if node.op == "<>":
                op = "!="
            elif node.op == "=":
                op = "=="
            elif node.op == "div":
                op = "/"
            elif node.op == "mod":
                op = "%"
            elif node.op == "and":
                op = "&&"
            elif node.op == "or":
                op = "||"
            return f"({left} {op} {right})"
        raise NotImplementedError(f"Unknown expr node: {type(node).__name__}")

