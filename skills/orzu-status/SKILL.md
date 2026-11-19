---
name: orzu-status
description: Еженедельный статус проектов группы Orzu Medical в общем репозитории orzu-medical/ai-projects. Участник отвечает на 3 вопроса, навык обновляет его STATUS.md и отправляет на GitHub. Тренер AIRL получает сводку по всем проектам. Запуск - /orzu-status, /orzu-status отчёт, /orzu-status задание <номер>.
argument-hint: "[пусто - мой статус · «отчёт» - сводка для тренера · «задание 07» - задание участнику]"
---

# /orzu-status

Общий репозиторий: `github.com/orzu-medical/ai-projects`. У каждого проекта своя папка в `projects/` (например `projects/07-rustamova-medical-history/`): код проекта, `STATUS.md` и, после домашки с `/airl-dwh`, файл `DWH.md`.

Репозиторий принадлежит Orzu Medical: он лежит в их GitHub-организации `orzu-medical`, код проектов принадлежит клинике. Тренеры AIRL работают в нём только по приглашению клиента. Ничего не копируй из него в другие репозитории, на другие сервисы или в свои заметки. Отчёт тренера сохраняется только внутри этого же репозитория.

Говори коротко и просто, без терминов. Если человек пишет по-узбекски, отвечай по-узбекски. Вопросы задавай по одному.

## Стадии

| Стадия | Название | Как проверить по папке |
|---|---|---|
| 0 | Идея | в папке только STATUS.md |
| 1 | MVP начат | есть код, но главная функция ещё не работает |
| 2 | MVP работает | главная функция работает, человек может показать экран |
| 3 | На GitHub | рабочий код лежит в своей папке репозитория |
| 4 | Есть ссылка | в STATUS.md есть ссылка, она открывается |
| 5 | Пользуются коллеги | человек назвал, кто из коллег пользуется |

Стадию ставь по файлам, а не по словам. Если человек говорит «работает», а кода нет, поставь ниже и мягко объясни почему.

## Если репозитория ещё нет на компьютере

Склонируй `https://github.com/orzu-medical/ai-projects` и перейди в папку. Если доступа нет, скажи: «Примите приглашение на GitHub, оно пришло на почту, или напишите тренеру свой логин GitHub».

## Режим 1. Участник: `/orzu-status`

1. `git pull --rebase`. Найди папку участника по `participant:` в `projects/*/STATUS.md` (спроси имя). Если проектов два, спроси, какой обновляем.
2. Если код проекта лежит не в его папке, предложи перенести его туда. Не копируй `node_modules`, `.env`, ключи, файлы базы с реальными данными.
3. Три вопроса, по одному:
   - Что получилось сделать за неделю?
   - Где застряли? (можно «нигде»)
   - Что сделаете к следующему уроку?
4. Посмотри файлы и поставь стадию по таблице. Если есть ссылка, проверь, что открывается. Если есть `DWH.md`, отметь это одной фразой.
5. Обнови `STATUS.md`: поля `stage`, `link`, `updated` (сегодня) и разделы «Что сделано», «Где застрял», «Следующий шаг». Раздел «Задание от тренера» не трогай.
6. Проверь, что в коммит не попадают ключи, пароли, `.env` и реальные данные пациентов. Если есть, убери и предупреди.
7. `git add projects/<папка>` (только своя папка), коммит `status: <папка> стадия N`, `git pull --rebase`, `git push`.
8. Одной фразой: стадия и следующий шаг.

## Режим 2. Тренер: `/orzu-status отчёт`

1. `git pull --rebase` в корне `orzu-medical/ai-projects`.
2. Запусти скрипт отчёта из корня репозитория: `python3 "${CLAUDE_SKILL_DIR}/scripts/status_report.py" --save`. Если такого файла нет, сохрани скрипт из раздела «Скрипт отчёта» во временный файл вне репозитория и запусти его так же. Скрипт печатает таблицу и сохраняет её в `reports/ДАТА.md`.
3. Под таблицей коротко:
   - кто стоит на месте (🔴) и что предложить каждому;
   - у кого блокер (🟡) и чем помочь;
   - у кого нет `DWH.md`: напомнить про домашку `/airl-dwh`;
   - у кого два проекта и ни один не дошёл до стадии 4: сначала довести один.
4. По одному следующему шагу каждому по стадии: 0-1 добить главную функцию MVP; 2 выложить код в свою папку; 3 получить рабочую ссылку; 4 дать двум коллегам попробовать; 5 подготовить показ результата.
5. Коммит `reports: ДАТА`, push.

## Режим 3. Тренер: `/orzu-status задание <номер>`

Открой `projects/<номер>-*/STATUS.md`, покажи статус, спроси новое задание (или предложи по стадии) и запиши в «Задание от тренера» с датой. Коммит и push.

## Правила

- Меняй только папку своего проекта.
- Данные пациентов только выдуманные. Если в папке есть реальные ФИО, телефоны, диагнозы пациентов или выгрузки из систем клиники, не коммить их: убери и скажи участнику.
- Ключи и пароли не коммить.
- В STATUS.md и в отчёте только рабочие сведения: имя участника, проект, стадия, что сделано, где застрял. Никаких личных данных сотрудников сверх этого.

## Скрипт отчёта

Запускать из корня `orzu-medical/ai-projects`. Только стандартная библиотека Python.

```python
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
```
