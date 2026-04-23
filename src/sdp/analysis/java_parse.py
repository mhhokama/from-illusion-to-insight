import re
from collections import defaultdict, deque
from typing import Dict, Tuple, List, Set


def find_java_classes(src: str) -> Dict[str, Tuple[int, int, str]]:
    src = src.replace("\r\n", "\n")
    lines = src.splitlines()
    classes = {}
    class_re = re.compile(r"^\s*(?:public|protected|private)?\s*class\s+(\w+)\b")
    stack = []

    for i, line in enumerate(lines, 1):
        m = class_re.search(line)
        if m:
            cname = m.group(1)
            full_name = cname if not stack else f"{stack[-1][2]}.{cname}"
            depth = line.count("{") - line.count("}")
            stack.append((cname, i, full_name, depth))
        for idx in range(len(stack)):
            cname, start, full_name, depth = stack[idx]
            depth += line.count("{") - line.count("}")
            stack[idx] = (cname, start, full_name, depth)
        while stack and stack[-1][3] <= 0:
            cname, start, full_name, _ = stack.pop()
            classes[cname] = (start, i, full_name)

    while stack:
        cname, start, full_name, _ = stack.pop()
        classes[cname] = (start, len(lines), full_name)

    return classes


def find_java_methods(src: str) -> Dict[str, Tuple[str, int, int, str]]:
    src = src.replace("\r\n", "\n")
    lines = src.splitlines()
    methods = {}
    method_re = re.compile(
        r"(?:public|protected|private)?\s*(?:static\s+)?[\w\<\>\[\]]+\s+([A-Za-z_]\w*)\s*\([^)]*\)\s*(?:throws\s+[^{]+)?\{"
    )

    classes = find_java_classes(src)
    class_ranges = [(name, cs, ce, full) for name, (cs, ce, full) in classes.items()]

    stack = []
    for i, line in enumerate(lines, 1):
        for m in method_re.finditer(line):
            name = m.group(1)
            before = line[:m.start()]
            if re.search(r"\bnew\s*$", before):
                continue
            uid = f"{name}@{i}"
            stack.append((uid, name, i, i, None, 0))
            methods[uid] = (name, i, i, None)
        if stack:
            opens = line.count("{")
            closes = line.count("}")
            delta = opens - closes
            if delta < 0:
                while -delta > 0 and stack:
                    uid, name, start, _, cls, _ = stack.pop()
                    methods[uid] = (name, start, i, cls)
                    delta += 1

    last_line = len(lines)
    for uid, name, start, _, cls, _ in stack:
        methods[uid] = (name, start, last_line, cls)

    for uid, (name, start, end, cls) in list(methods.items()):
        for cname, cs, ce, full in class_ranges:
            if cs <= start <= ce:
                methods[uid] = (name, start, end, full)
                break

    return methods


def extract_changed_entities(diffs: Dict[str, List[Tuple]], methods: Dict[str, Tuple[str, int, int, str]], classes: Dict[str, Tuple[int, int, str]]) -> Tuple[Set[str], Set[str]]:
    changed_lines = set()
    for ln, _ in diffs.get("removed", []):
        changed_lines.add(ln)
    for ln, _ in diffs.get("added", []):
        changed_lines.add(ln)
    for old_ln, _, new_ln, _ in diffs.get("changed", []):
        changed_lines.add(old_ln)
        changed_lines.add(new_ln)

    changed_methods = {
        mname
        for _, (mname, start, end, _) in methods.items()
        if any(start <= ln <= end for ln in changed_lines)
    }

    changed_classes = {
        cname
        for cname, (start, end, _) in classes.items()
        if any(start <= ln <= end for ln in changed_lines)
    }

    return changed_methods, changed_classes


def find_method_calls(src: str, methods: Dict[str, Tuple[str, int, int, str]]) -> Dict[str, Set[str]]:
    src_lines = src.splitlines()
    call_re = re.compile(r"\b([A-Za-z_]\w*)\s*\(")
    line_to_method = {}
    for uid, (mname, start, end, _) in methods.items():
        for ln in range(start, end + 1):
            line_to_method[ln] = mname

    mapping = defaultdict(set)
    for i, line in enumerate(src_lines, 1):
        caller = line_to_method.get(i)
        if not caller:
            continue
        for callee in call_re.findall(line):
            if callee in {"if", "for", "while", "switch", "new", "catch", "try", "throw", "return", "super"}:
                continue
            mapping[caller].add(callee)
    return mapping


def expand_call_graph(context_methods: Set[str], calls: Dict[str, Set[str]], methods: Dict[str, Tuple[str, int, int, str]], depth: int) -> Set[str]:
    queue = deque([(m, 0) for m in context_methods])
    visited = set(context_methods)

    while queue:
        method_name, level = queue.popleft()
        if level >= depth:
            continue
        for callee in calls.get(method_name, set()):
            if callee in visited:
                continue
            if any(val[0] == callee for val in methods.values()):
                visited.add(callee)
                queue.append((callee, level + 1))
        for caller, callees in calls.items():
            if method_name in callees and caller not in visited:
                visited.add(caller)
                queue.append((caller, level + 1))

    return visited


def build_context_snippets(src: str, methods: Dict[str, Tuple[str, int, int, str]], context_method_names: Set[str], max_lines: int = 400) -> str:
    lines = src.splitlines()
    output = []
    for _, (name, start, end, cls) in methods.items():
        if name in context_method_names:
            snippet = "\n".join(lines[start - 1 : end])
            output.append(f"// Context: method {name} in class {cls}\n{snippet}")

    output_lines = "\n\n".join(output).splitlines()
    if len(output_lines) > max_lines:
        output_lines = output_lines[:max_lines]
    return "\n".join(output_lines)


def extract_relevant_context(src: str, diffs: Dict[str, List[Tuple]], depth: int = 1, max_lines: int = 400) -> str:
    classes = find_java_classes(src)
    methods = find_java_methods(src)
    calls = find_method_calls(src, methods)
    changed_methods, _ = extract_changed_entities(diffs, methods, classes)
    context_methods = expand_call_graph(changed_methods, calls, methods, depth)
    return build_context_snippets(src, methods, context_methods, max_lines)
