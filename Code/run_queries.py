import json
import os 
import re
import statistics
import sys
import time

import mysql.connector

DB = dict(host="localhost", port=3306, user="-", password="-", database="GDELT")

def load_queries(path="queries.sql"):
    text = open(path, encoding="utf-8").read()
    header = re.compile(r"^[ \t]*--[ \t]*(?:QUERY[ \t]*|Q)(\d+)[ \t]*[.:)]?[ \t]*(.*)$",re.IGNORECASE | re.MULTILINE)
    marks = list(header.finditer(text))
    queries = {}
    for i, m in enumerate(marks):
        end = marks[i+1].start() if i+1 < len(marks) else len(text)
        body = "\n".join(l for l in text[m.end():end].split("\n") if not l.strip().startswith("--")).strip()
        body = re.sub(r"^\s*USE\s+\w+\s*;", "", body, flags=re.I).strip()
        if body:
            queries[f"Q{m.group(1)}"] = (m.group(2).strip(), body.rstrip().rstrip(";"))
    return queries

def run_query(query, sql):
    for statement in (s.strip() for s in sql.split(";")):
        if statement:
            query.execute(statement)
            try:
                query.fetchall()
            except mysql.connector.Error:
                pass

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "before"
    queries = load_queries()
    connector = mysql.connector.connect(**DB)
    query = connector.cursor()

    output = {}
    for name in sorted(queries, key=lambda n: int(n[1:])):
        title, sql = queries[name]
        run_query(query, sql)
        samples = []
        for i in range(5):
            start = time.perf_counter()
            run_query(query,sql)
            samples.append((time.perf_counter() - start) * 1000)
        output[name] = round(statistics.median(samples), 1)
        print(f"{name} {output[name]:9.1f} ms {title[:48]}")

    json.dump(output, open(f"timings_{mode}.json", "w"), indent=2)
    print(f"\nwrote timings_{mode}.json")

    if mode == "after" and os.path.exists("timings_before.json"):
        before = json.load(open("timings_before.json"))
        print(f"\n{'Query':<8}{'Before(ms)':>13}{'After(ms)':>13}{'Speedup':>11}")
        print("-" * 50)
        for name in sorted(output, key=lambda n: int(n[1:])):
            if name in before:
                b, a = before[name], output[name]
                print(f"{name:<8}{b:>13.1f}{a:>13.1f}{b/a:>10.2f}x")
        query.close()
        connector.close()

if __name__ == "__main__":
    main()