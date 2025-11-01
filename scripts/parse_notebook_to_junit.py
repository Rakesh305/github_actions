#!/usr/bin/env python3
"""
parse_notebook_to_junit.py
~~~~~~~~~~~~~~~~~~~~~~~~~~

A tiny helper that turns the executed notebook into a JUnit XML file.

Usage (called from the GitHub Action):
  python3 parse_notebook_to_junit.py \
      /path/to/exec-ui-test.ipynb \
      /tmp/junit-results.xml
"""

import json
import sys
import pathlib


def notebook_to_junit(exec_notebook: pathlib.Path, out_xml: pathlib.Path):
    # Load the executed notebook
    with exec_notebook.open("r", encoding="utf-8") as f:
        nb = json.load(f)

    test_cases = []
    failures = 0

    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue

        # Grab the original source line as the test name
        test_name = cell["source"][0].strip() if cell["source"] else "Unnamed Test"

        # Grab the first output (should be the last line of the code cell)
        last_output = ""
        if cell.get("outputs"):
            # Selenium / Helium outputs are not captured by Jupyter.
            # Instead we look for any "assert" failures via the exception message.
            # The notebook prints nothing on success, so we treat an empty `outputs` list as success.
            pass

        # Detect failure by inspecting cell outputs for exception traces
        # (nbconvert stores exception tracebacks in `e.value` or `e.traceback`)
        failed = False
        for out in cell.get("outputs", []):
            if out.get("output_type") == "error":
                failed = True
                exc_msg = out.get("ename", "Exception") + ": " + out.get("evalue", "")
                break

        if failed:
            failures += 1
            test_cases.append({"name": test_name, "result": "FAIL", "message": exc_msg})
        else:
            test_cases.append({"name": test_name, "result": "PASS"})

    # Build a simple JUnit XML structure
    root = pathlib.Path(out_xml).parent
    root.mkdir(parents=True, exist_ok=True)

    xml = f"""<?xml version="1.0" encoding="utf-8"?>
<testsuite name="Helium UI Tests" tests="{len(test_cases)}" failures="{failures}">
"""
    for tc in test_cases:
        if tc["result"] == "FAIL":
            xml += f'  <testcase classname="ui_test_sample" name="{tc["name"]}"><failure message="{tc["message"]}"/></testcase>\n'
        else:
            xml += f'  <testcase classname="ui_test_sample" name="{tc["name"]}"/>\n'

    xml += "</testsuite>\n"

    with out_xml.open("w", encoding="utf-8") as f:
        f.write(xml)

    print(f"✅ JUnit XML written to {out_xml}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python parse_notebook_to_junit.py <executed_ipynb> <output_xml>")
        sys.exit(1)

    notebook_to_junit(pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]))
