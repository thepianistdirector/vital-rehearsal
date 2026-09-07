#!/usr/bin/env python3
"""Validate Vital Rehearsal's repository-owned plan without dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


TASK_ID = r"VR-[A-Z0-9-]+"
ALLOWED_STATUSES = {
    "PLANNED",
    "READY_FOR_REVIEW",
    "DONE",
    "IN_PROGRESS",
    "IN PROGRESS",
    "IMPLEMENTED",
    "AUTOMATED PASS",
    "RUNTIME VERIFIED",
    "USER VALIDATED",
    "RELEASE VERIFIED",
    "BLOCKED",
    "FAILED",
    "NOT TESTED",
    "HOLD",
}
FOUNDATION_IDS = ("VR-F01", "VR-F02", "VR-F03")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="repository root to validate (defaults to this script's parent repository)",
    )
    return parser.parse_args()


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing required file: {path}")
        return {}
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {path}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path} must contain a JSON object")
        return {}
    return value


def parse_task_markdown(path: Path, errors: list[str]) -> dict[str, dict]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"missing required file: {path}")
        return {}

    header = re.compile(rf"^## ({TASK_ID}) — (.+)$", re.MULTILINE)
    matches = list(header.finditer(text))
    tasks: dict[str, dict] = {}
    for index, match in enumerate(matches):
        task_id, title = match.groups()
        if task_id in tasks:
            errors.append(f"{path}: duplicate section for {task_id}")
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end() : end]
        wave_status = re.search(
            r"^- Wave: ([0-9]+); status: \*\*([A-Z_ ]+)\*\*;",
            body,
            re.MULTILINE,
        )
        dependencies = re.search(r"^- Dependencies: (.+)\.$", body, re.MULTILINE)
        acceptance = re.search(r"^- Acceptance: (.+)$", body, re.MULTILINE)
        if not wave_status:
            errors.append(f"{path}: {task_id} lacks parseable wave/status")
        if not dependencies:
            errors.append(f"{path}: {task_id} lacks parseable dependencies")
        if not acceptance:
            errors.append(f"{path}: {task_id} lacks parseable acceptance")
        dep_ids = (
            []
            if not dependencies or dependencies.group(1).strip().lower() == "none"
            else re.findall(TASK_ID, dependencies.group(1))
        )
        tasks[task_id] = {
            "title": title,
            "wave": int(wave_status.group(1)) if wave_status else None,
            "status": wave_status.group(2) if wave_status else None,
            "dependsOn": dep_ids,
            "acceptance": acceptance.group(1).strip() if acceptance else None,
        }
    return tasks


def parse_status_table(path: Path, errors: list[str]) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"missing required file: {path}")
        return {}
    rows = re.findall(
        rf"^\| ({TASK_ID}) \| \*\*([A-Z_ ]+)\*\* \|",
        text,
        re.MULTILINE,
    )
    statuses: dict[str, str] = {}
    for task_id, status in rows:
        if task_id in statuses:
            errors.append(f"{path}: duplicate status row for {task_id}")
        statuses[task_id] = status
    return statuses


def check_task_json(
    plan: dict, errors: list[str]
) -> tuple[dict[str, dict], bool]:
    structurally_valid = True
    schema_version = plan.get("schemaVersion")
    if type(schema_version) is not int or schema_version != 1:
        errors.append("plan/tasks.json: schemaVersion must be the integer 1")
        structurally_valid = False
    if plan.get("project") != "vital-rehearsal":
        errors.append("plan/tasks.json: project must be vital-rehearsal")
        structurally_valid = False
    if not isinstance(plan.get("contractVersion"), str) or not plan["contractVersion"]:
        errors.append("plan/tasks.json: contractVersion must be a non-empty string")
        structurally_valid = False
    raw_tasks = plan.get("tasks")
    if not isinstance(raw_tasks, list) or not raw_tasks:
        errors.append("plan/tasks.json: tasks must be a non-empty array")
        return {}, False

    tasks: dict[str, dict] = {}
    required = {
        "id",
        "wave",
        "title",
        "status",
        "dependsOn",
        "ownedPaths",
        "acceptance",
    }
    for index, task in enumerate(raw_tasks):
        if not isinstance(task, dict):
            errors.append(f"plan/tasks.json: task at index {index} is not an object")
            structurally_valid = False
            continue
        missing = sorted(required - task.keys())
        if missing:
            errors.append(
                f"plan/tasks.json: task at index {index} missing {', '.join(missing)}"
            )
            structurally_valid = False
            continue
        task_id = task["id"]
        if not isinstance(task_id, str) or not re.fullmatch(TASK_ID, task_id):
            errors.append(f"plan/tasks.json: invalid task id {task_id!r}")
            structurally_valid = False
            continue
        if task_id in tasks:
            errors.append(f"plan/tasks.json: duplicate task id {task_id}")
            structurally_valid = False
            continue
        if type(task["wave"]) is not int or task["wave"] < 0:
            errors.append(f"plan/tasks.json: {task_id} has invalid wave")
            structurally_valid = False
        if (
            not isinstance(task["status"], str)
            or task["status"] not in ALLOWED_STATUSES
        ):
            errors.append(
                f"plan/tasks.json: {task_id} has unsupported status {task['status']!r}"
            )
            structurally_valid = False
        if not isinstance(task["dependsOn"], list) or not all(
            isinstance(item, str) and re.fullmatch(TASK_ID, item)
            for item in task["dependsOn"]
        ):
            errors.append(
                f"plan/tasks.json: {task_id} dependsOn must be an array of task IDs"
            )
            structurally_valid = False
        if (
            not isinstance(task["ownedPaths"], list)
            or not task["ownedPaths"]
            or not all(
                isinstance(item, str) and item.strip() for item in task["ownedPaths"]
            )
        ):
            errors.append(f"plan/tasks.json: {task_id} ownedPaths must be non-empty paths")
            structurally_valid = False
        if not isinstance(task["title"], str) or not task["title"].strip():
            errors.append(f"plan/tasks.json: {task_id} title is empty")
            structurally_valid = False
        if not isinstance(task["acceptance"], str) or not task["acceptance"].strip():
            errors.append(f"plan/tasks.json: {task_id} acceptance is empty")
            structurally_valid = False
        tasks[task_id] = task
    return tasks, structurally_valid


def check_dependencies(tasks: dict[str, dict], errors: list[str]) -> None:
    for task_id, task in tasks.items():
        dependencies = task.get("dependsOn", [])
        if len(dependencies) != len(set(dependencies)):
            errors.append(f"plan/tasks.json: {task_id} repeats a dependency")
        for dependency in dependencies:
            if dependency == task_id:
                errors.append(f"plan/tasks.json: {task_id} depends on itself")
            elif dependency not in tasks:
                errors.append(
                    f"plan/tasks.json: {task_id} has unknown dependency {dependency}"
                )

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str, stack: list[str]) -> None:
        if task_id in visiting:
            cycle_start = stack.index(task_id)
            errors.append(
                "plan/tasks.json: dependency cycle: "
                + " -> ".join(stack[cycle_start:] + [task_id])
            )
            return
        if task_id in visited:
            return
        visiting.add(task_id)
        stack.append(task_id)
        for dependency in tasks[task_id].get("dependsOn", []):
            if dependency in tasks:
                visit(dependency, stack)
        stack.pop()
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in tasks:
        visit(task_id, [])


def check_projection(
    json_tasks: dict[str, dict],
    markdown_tasks: dict[str, dict],
    statuses: dict[str, str],
    errors: list[str],
) -> None:
    json_ids = set(json_tasks)
    markdown_ids = set(markdown_tasks)
    status_ids = set(statuses)
    if json_ids != markdown_ids:
        errors.append(
            "TASKS.md and plan/tasks.json task IDs differ: "
            f"JSON-only={sorted(json_ids - markdown_ids)}, "
            f"Markdown-only={sorted(markdown_ids - json_ids)}"
        )
    if json_ids != status_ids:
        errors.append(
            "STATUS.md and plan/tasks.json task IDs differ: "
            f"JSON-only={sorted(json_ids - status_ids)}, "
            f"Status-only={sorted(status_ids - json_ids)}"
        )

    for task_id in sorted(json_ids & markdown_ids):
        source = json_tasks[task_id]
        projection = markdown_tasks[task_id]
        for field in ("title", "wave", "status", "dependsOn", "acceptance"):
            if source.get(field) != projection.get(field):
                errors.append(
                    f"TASKS.md: {task_id} {field} differs from plan/tasks.json"
                )
    for task_id in sorted(json_ids & status_ids):
        if json_tasks[task_id].get("status") != statuses[task_id]:
            errors.append(
                f"STATUS.md: {task_id} status differs from plan/tasks.json"
            )


def check_roadmap(root: Path, tasks: dict[str, dict], errors: list[str]) -> None:
    path = root / "ROADMAP.md"
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"missing required file: {path}")
        return
    wave_headers = list(
        re.finditer(r"^## Wave ([0-9]+): .+$", text, re.MULTILINE)
    )
    declared_waves = [int(match.group(1)) for match in wave_headers]
    duplicate_waves = sorted(
        {wave for wave in declared_waves if declared_waves.count(wave) > 1}
    )
    if duplicate_waves:
        errors.append(f"ROADMAP.md: duplicate wave headings {duplicate_waves}")

    task_waves = {task["wave"] for task in tasks.values()}
    if set(declared_waves) != task_waves:
        errors.append(
            "ROADMAP.md wave headings differ from task waves: "
            f"Task-only={sorted(task_waves - set(declared_waves))}, "
            f"Roadmap-only={sorted(set(declared_waves) - task_waves)}"
        )

    listed: list[str] = []
    for index, match in enumerate(wave_headers):
        wave = int(match.group(1))
        end = (
            wave_headers[index + 1].start()
            if index + 1 < len(wave_headers)
            else len(text)
        )
        section_ids = re.findall(
            rf"^- \*\*({TASK_ID}):", text[match.end() : end], re.MULTILINE
        )
        listed.extend(section_ids)
        for task_id in section_ids:
            if task_id in tasks and tasks[task_id]["wave"] != wave:
                errors.append(
                    f"ROADMAP.md: {task_id} is listed under Wave {wave} "
                    f"but plan/tasks.json declares Wave {tasks[task_id]['wave']}"
                )
    duplicates = sorted({task_id for task_id in listed if listed.count(task_id) > 1})
    if duplicates:
        errors.append(f"ROADMAP.md: duplicate task entries {duplicates}")
    if set(listed) != set(tasks):
        errors.append(
            "ROADMAP.md and plan/tasks.json task IDs differ: "
            f"JSON-only={sorted(set(tasks) - set(listed))}, "
            f"Roadmap-only={sorted(set(listed) - set(tasks))}"
        )


def check_foundation(tasks: dict[str, dict], errors: list[str]) -> None:
    for task_id in FOUNDATION_IDS:
        if task_id not in tasks:
            errors.append(f"missing foundation task {task_id}")
            return
        if tasks[task_id].get("wave") != 0:
            errors.append(f"{task_id} must remain in Wave 0")
        if tasks[task_id].get("status") not in {"READY_FOR_REVIEW", "DONE"}:
            errors.append(f"{task_id} must be READY_FOR_REVIEW or DONE")

    expected = {
        "VR-F01": [],
        "VR-F02": ["VR-F01"],
        "VR-F03": ["VR-F02"],
    }
    for task_id, dependencies in expected.items():
        if tasks.get(task_id, {}).get("dependsOn") != dependencies:
            errors.append(f"{task_id} must depend on {dependencies}")

    if tasks.get("VR-F02", {}).get("status") == "DONE":
        if tasks.get("VR-F01", {}).get("status") != "DONE":
            errors.append("VR-F02 cannot be DONE before VR-F01")
    if tasks.get("VR-F03", {}).get("status") == "DONE":
        if tasks.get("VR-F02", {}).get("status") != "DONE":
            errors.append("VR-F03 cannot be DONE before VR-F02")
    if "VR-001" in tasks and "VR-F03" not in tasks["VR-001"].get("dependsOn", []):
        errors.append("VR-001 must depend on VR-F03")


def check_next_packet(root: Path, errors: list[str]) -> None:
    path = root / "plan" / "NEXT_WORK.md"
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"missing required file: {path}")
        return
    required_phrases = (
        "VR-001",
        "Candidate A: Pulse",
        "Candidate B: published CellML/SED-ML model",
        "Selection questions",
        "Acceptance matrix",
        "No numerical tolerance",
        "patient-level data",
        "qualified physiology reviewer",
        "python3 tools/validate_plan.py",
    )
    for phrase in required_phrases:
        if phrase not in text:
            errors.append(f"plan/NEXT_WORK.md: missing required contract phrase {phrase!r}")
    question_count = len(re.findall(r"^[0-9]+\. \*\*", text, re.MULTILINE))
    if question_count < 10:
        errors.append(
            "plan/NEXT_WORK.md: expected at least 10 explicit benchmark questions"
        )


def check_local_links(root: Path, errors: list[str]) -> None:
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for raw_target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            target = raw_target.strip()
            if (
                not target
                or target.startswith("#")
                or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target)
            ):
                continue
            without_anchor = unquote(target.split("#", 1)[0])
            resolved = (path.parent / without_anchor).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{path.relative_to(root)}: link escapes repository: {target}")
                continue
            if not resolved.exists():
                errors.append(
                    f"{path.relative_to(root)}: broken local link target {target}"
                )


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    errors: list[str] = []
    plan_path = root / "plan" / "tasks.json"
    plan = load_json(plan_path, errors)
    tasks, task_structure_valid = (
        check_task_json(plan, errors) if plan else ({}, False)
    )

    state_authority = plan.get("stateAuthority") if plan else None
    state_authority_valid = True
    expected_authority = (root / "STATUS.md").resolve()
    if state_authority != "../STATUS.md":
        errors.append(
            "plan/tasks.json: stateAuthority must be exactly ../STATUS.md"
        )
        state_authority_valid = False
    elif (plan_path.parent / state_authority).resolve() != expected_authority:
        errors.append("plan/tasks.json: stateAuthority must resolve to root STATUS.md")
        state_authority_valid = False
    elif not expected_authority.is_file():
        errors.append("plan/tasks.json: authoritative root STATUS.md does not exist")
        state_authority_valid = False

    markdown_tasks = parse_task_markdown(root / "TASKS.md", errors)
    statuses = parse_status_table(root / "STATUS.md", errors)
    if tasks and task_structure_valid and state_authority_valid:
        check_dependencies(tasks, errors)
        check_projection(tasks, markdown_tasks, statuses, errors)
        check_roadmap(root, tasks, errors)
        check_foundation(tasks, errors)
    check_next_packet(root, errors)
    check_local_links(root, errors)

    if errors:
        print(f"Vital Rehearsal plan validation FAILED ({len(errors)} issue(s)):")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Vital Rehearsal plan validation PASS: "
        f"{len(tasks)} synchronized tasks, acyclic dependencies, "
        "valid foundation states, executable next packet, and resolved local links."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
