#!/usr/bin/env python3
"""Сводка прогресса по всем проектам Orzu Medical.

Запуск из корня репозитория orzu-medical/ai-projects:
    python3 <папка навыка>/scripts/status_report.py [--save]

Читает projects/*/STATUS.md, смотрит, есть ли в папке DWH.md,
берёт дату последнего коммита и печатает таблицу в Markdown.
С флагом --save пишет её в reports/ДАТА.md. Только стандартная библиотека.
"""
import datetime as dt
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path.cwd()
PROJECTS = ROOT / "projects"
STAGES = {
    0: "Идея",
    1: "MVP начат",
    2: "MVP работает",
    3: "На GitHub",
    4: "Есть ссылка",
    5: "Пользуются коллеги",
}
STALE_DAYS = 7


def parse_status(path):
    text = path.read_text(encoding="utf-8")
    meta, body = {}, text
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        body = m.group(2)
    sections = {}
    for sm in re.finditer(r"^## (.+?)\n(.*?)(?=^## |\Z)", body, re.S | re.M):
        sections[sm.group(1).strip()] = sm.group(2).strip()
    return meta, sections


def last_commit(folder):
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(folder)],
            cwd=ROOT, capture_output=True, text=True, timeout=10,
        ).stdout.strip()
        if out:
            return dt.date.fromisoformat(out)
    except Exception:
        pass
    return None


def first_line(text):
    for line in (text or "").splitlines():
        line = line.strip().lstrip("-").strip()
        if line and not line.startswith("("):
            return line
    return "-"


def main():
    if not PROJECTS.is_dir():
        sys.exit("Нет папки projects/. Запустите из корня репозитория orzu-medical/ai-projects.")
    today = dt.date.today()
    rows, alerts = [], []
    counts = {s: 0 for s in STAGES}
    dwh_done = 0
    for folder in sorted(p for p in PROJECTS.iterdir() if p.is_dir()):
        status = folder / "STATUS.md"
        if not status.exists():
            alerts.append(f"{folder.name}: нет STATUS.md")
            continue
        meta, sec = parse_status(status)
        try:
            stage = int(meta.get("stage", "0"))
        except ValueError:
            stage = 0
        counts[stage] = counts.get(stage, 0) + 1
        dwh = any(folder.rglob("DWH.md"))
        dwh_done += dwh
        commit = last_commit(folder)
        days = (today - commit).days if commit else None
        stuck = first_line(sec.get("Где застрял"))
        flag = "🟢"
        if days is None or days > STALE_DAYS:
            flag = "🔴"
            alerts.append(f"{meta.get('participant', folder.name)}: нет новых коммитов больше {STALE_DAYS} дней")
        elif stuck not in ("-", "нет", "Нет", "нигде", "Нигде"):
            flag = "🟡"
        rows.append((
            folder.name.split("-")[0],
            meta.get("participant", "?"),
            meta.get("project", "?"),
            f"{stage} · {STAGES.get(stage, '?')}",
            "есть" if dwh else "нет",
            commit.isoformat() if commit else "нет коммитов",
            stuck,
            first_line(sec.get("Следующий шаг")),
            flag,
        ))

    out = [f"# Прогресс Orzu Medical · {today.isoformat()}", ""]
    out.append("| № | Участник | Проект | Стадия | DWH.md | Последний коммит | Где застрял | Следующий шаг | |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    out += ["| " + " | ".join(r) + " |" for r in rows]
    out += ["", "## По стадиям", ""]
    out += [f"- {s} · {name}: {counts.get(s, 0)}" for s, name in STAGES.items()]
    out += ["", f"Схема данных (DWH.md) готова у {dwh_done} из {len(rows)}.", "", "## Требуют внимания", ""]
    out += [f"- {a}" for a in alerts] or ["- все в работе"]
    report = "\n".join(out) + "\n"
    print(report)
    if "--save" in sys.argv:
        rep_dir = ROOT / "reports"
        rep_dir.mkdir(exist_ok=True)
        (rep_dir / f"{today.isoformat()}.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
