#!/usr/bin/env python3
"""Validate Vital Rehearsal's repository-owned plan without dependencies."""

from __future__ import annotations

import argparse
import hashlib
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
    if type(schema_version) is not int or schema_version != 2:
        errors.append("plan/tasks.json: schemaVersion must be the integer 2")
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
    required_status_ids = set(FOUNDATION_IDS) | {f"VR-{n:03d}" for n in range(1, 25)}
    if not required_status_ids <= status_ids or not status_ids <= json_ids:
        errors.append(
            "STATUS.md and plan/tasks.json task IDs differ: "
            f"Required-only={sorted(required_status_ids - status_ids)}, "
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
        if any(part in {".git", ".venv", ".cache", "runs", "artifacts", "__pycache__"} for part in path.relative_to(root).parts) or "lineage" in path.relative_to(root).parts:
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


RELEASE_ORDER = {'foundation': -1, '0.1': 0, 'later 0.x': 1, 'long-term': 2, 'exploratory': 3}
FROZEN_COMMIT = '9fa99f392c93f6f1e33a2cd85b9348cb68afe39e'
FROZEN_LEDGER_SHA256 = '7814846d68842323eb22efb145f2fd29205b5d31d438a8022f570d9fcf61c3f4'
# Load-bearing 0.1 admission and release edges are an acceptance contract, not
# inferred from titles. Control-only work intentionally has no admission edge.
CRITICAL_DEPENDENCIES = {
    **{f'VR-W03-{n:02d}': {'VR-W01-08', 'VR-W02-08'} for n in range(1, 9)},
    'VR-W04-08': {'VR-W03-08'},
    'VR-W05-05': {'VR-W04-08', 'VR-W05-02', 'VR-W05-03', 'VR-W05-04'},
    'VR-W05-06': {'VR-W05-05'},
    'VR-W05-08': {'VR-W05-05', 'VR-W05-06'},
    'VR-W05-07': {'VR-W05-08'},
    'VR-W05-09': {'VR-W05-07', 'VR-W05-08'},
}


def check_expansion(root: Path, plan: dict, tasks: dict, errors: list[str]) -> None:
    lineage = root / 'plan/lineage/foundation-2026-09-07'
    frozen = load_json(lineage / 'plan__tasks.json', errors)
    manifest = load_json(lineage / 'manifest.json', errors)
    originals = {t['id']: t for t in frozen.get('tasks', [])}
    frozen_path = lineage / 'plan__tasks.json'
    if not frozen_path.is_file() or hashlib.sha256(frozen_path.read_bytes()).hexdigest() != FROZEN_LEDGER_SHA256:
        errors.append('lineage: original ledger differs from the pinned source bytes')
    expected_ids = set(FOUNDATION_IDS) | {f'VR-{n:03d}' for n in range(1, 25)}
    if set(originals) != expected_ids:
        errors.append('lineage: expected exactly the original 27 source identities')
    if manifest.get('sourceCommit') != FROZEN_COMMIT:
        errors.append('lineage: unexpected frozen source commit')
    for path, metadata in manifest.get('files', {}).items():
        target = (root / path).resolve()
        if not target.is_relative_to(lineage.resolve()):
            errors.append('lineage: manifest path escapes frozen directory'); continue
        if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != metadata.get('sha256'):
            errors.append(f'lineage: changed or absent frozen source {path}')
    for task_id, original in originals.items():
        if tasks.get(task_id) != original:
            errors.append(f'lineage: original task object changed: {task_id}')
    # Preserve original structural, roadmap and foundation checks against immutable source.
    check_dependencies(originals, errors)
    check_roadmap(lineage, originals, errors)
    check_foundation(tasks, errors)
    metadata = plan.get('legacyTaskMetadata')
    if not isinstance(metadata, dict) or set(metadata) != expected_ids:
        errors.append('legacyTaskMetadata must cover exactly the original 27 identities'); metadata = {}
    new = {i: t for i, t in tasks.items() if i not in expected_ids}
    for task_id, required in CRITICAL_DEPENDENCIES.items():
        if not required <= set(tasks.get(task_id, {}).get('dependsOn', [])):
            errors.append(f'{task_id}: load-bearing admission/release prerequisite outcome coverage missing')
    native_count = len(new) + len(FOUNDATION_IDS)
    if not 200 <= native_count <= 400:
        errors.append(f'expected 200–400 nonduplicated native outcomes, found {native_count}')
    known_refs = set(plan.get('sourceRegistry', {})) | expected_ids
    required_text = ('outcome', 'featureArea', 'targetRelease', 'requirementKind')
    titles: dict[str, str] = {}; outcomes: dict[str, str] = {}
    for task_id, task in new.items():
        for field in required_text:
            if not isinstance(task.get(field), str) or not task[field].strip():
                errors.append(f'{task_id}: missing nonempty {field}')
        if task.get('targetRelease') not in RELEASE_ORDER:
            errors.append(f'{task_id}: invalid release horizon')
        for field in ('sourceRefs', 'riskEvidenceNeeds'):
            value = task.get(field)
            if not isinstance(value, list) or not value or not all(isinstance(v, str) and v.strip() for v in value):
                errors.append(f'{task_id}: {field} must be a nonempty string list')
        for field in ('textualPrerequisites', 'evidence'):
            value = task.get(field)
            if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
                errors.append(f'{task_id}: {field} must be a string list')
        refs = task.get('sourceRefs', [])
        if isinstance(refs, list) and any(not isinstance(ref, str) or ref not in known_refs for ref in refs):
            errors.append(f'{task_id}: unknown source reference')
        if task.get('status') not in {'PLANNED', 'NOT TESTED'} and not task.get('evidence'):
            errors.append(f'{task_id}: non-planned status requires evidence')
        for field, seen in (('title', titles), ('outcome', outcomes)):
            value = task.get(field)
            if isinstance(value, str):
                normalized = re.sub(r'\W+', ' ', value.casefold()).strip()
                if normalized in seen:
                    errors.append(f'duplicate {field}: {task_id} and {seen[normalized]}')
                seen[normalized] = task_id
        for dependency in task.get('dependsOn', []):
            if dependency in expected_ids and dependency not in FOUNDATION_IDS:
                errors.append(f'{task_id}: successor depends on duplicate legacy aggregate {dependency}')
            other = tasks.get(dependency, {})
            if dependency in new and RELEASE_ORDER.get(other.get('targetRelease'), 99) > RELEASE_ORDER.get(task.get('targetRelease'), -1):
                errors.append(f'{task_id}: prerequisite {dependency} has a later release horizon')
            if dependency in new and other['wave'] > task['wave']:
                errors.append(f'{task_id}: prerequisite {dependency} is in a later wave')
    waves = plan.get('waves')
    if not isinstance(waves, list) or not 1 <= len(waves) <= 32:
        errors.append('waves: expected at most 32 native waves'); waves = []
    wave_ids=[]; assigned=[]; wave_order=[]
    for wave in waves:
        if not isinstance(wave, dict): errors.append('wave must be an object'); continue
        wave_id=wave.get('id'); wave_ids.append(wave_id)
        if type(wave_id) is not int:
            errors.append('wave id must be an integer')
        if not isinstance(wave.get('name'), str) or not 1 <= len(wave['name']) <= 80:
            errors.append(f'wave {wave_id}: name must have 1–80 characters')
        if not isinstance(wave.get('outcome'), str) or not wave['outcome'].strip():
            errors.append(f'wave {wave_id}: missing outcome')
        if wave.get('targetRelease') not in RELEASE_ORDER:
            errors.append(f'wave {wave_id}: invalid horizon')
        wave_order.append(wave_id)
        for field in ('taskIds', 'exitEvidence'):
            if not isinstance(wave.get(field), list) or not wave[field] or not all(isinstance(x, str) and x for x in wave[field]):
                errors.append(f'wave {wave_id}: missing {field}')
        entries = wave.get('entryDependencies', [])
        if not isinstance(entries, list) or not all(isinstance(x, str) and x in tasks for x in entries):
            errors.append(f'wave {wave_id}: dangling entry dependency'); entries=[]
        ids = wave.get('taskIds', [])
        if not isinstance(ids, list): continue
        assigned.extend(i for i in ids if isinstance(i, str))
        for task_id in ids:
            if not isinstance(task_id, str) or task_id not in tasks:
                errors.append(f'wave {wave_id}: unknown task'); continue
            task = tasks[task_id]
            if task['wave'] != wave_id:
                errors.append(f'wave {wave_id}: mismatched task assignment {task_id}')
            if task_id in new and task.get('targetRelease') != wave.get('targetRelease'):
                errors.append(f'wave {wave_id}: task release-scope mismatch {task_id}')
        # Entry gates must be represented in the assigned tasks' transitive prerequisite graph.
        covered=set()
        def ancestors(task_id: str) -> None:
            if task_id in covered or task_id not in tasks: return
            covered.add(task_id)
            for dep in tasks[task_id]['dependsOn']: ancestors(dep)
        for i in ids:
            if isinstance(i, str): ancestors(i)
        if set(entries)-covered:
            errors.append(f'wave {wave_id}: entry prerequisite outcome coverage missing')
    if len(wave_ids) != len(set(str(i) for i in wave_ids)):
        errors.append('duplicate wave IDs')
    if all(type(i) is int for i in wave_order) and wave_order != sorted(wave_order):
        errors.append('wave ordering is not ascending')
    if len(assigned) != len(set(assigned)):
        errors.append('duplicate native task assignment')
    if set(assigned) != set(new) | set(FOUNDATION_IDS):
        errors.append('orphan or duplicate historical outcome in native wave assignment')
    # Every successor must be reachable from the accepted foundation.
    def reaches_foundation(task_id: str, visited: set[str]) -> bool:
        if task_id in FOUNDATION_IDS: return True
        if task_id in visited or task_id not in tasks: return False
        return any(reaches_foundation(d, visited | {task_id}) for d in tasks[task_id]['dependsOn'])
    for task_id in new:
        if not reaches_foundation(task_id, set()): errors.append(f'orphan task: {task_id} has no foundation path')
    mappings=plan.get('sourceMappings')
    if not isinstance(mappings, list): errors.append('missing source mappings'); mappings=[]
    mapped=[]
    for mapping in mappings:
        if not isinstance(mapping, dict): errors.append('source mapping must be object'); continue
        source=mapping.get('sourceId'); mapped.append(source)
        if source not in originals: errors.append('unknown mapping source'); continue
        if mapping.get('sourceKey') != 'vital-rehearsal:'+source or mapping.get('sourceRevision') != 'foundation-2026-09-07':
            errors.append(f'{source}: changed source identity/revision')
        if mapping.get('treatment') not in {'retained','expanded','split','merged','deferred','superseded'} or not mapping.get('reason'):
            errors.append(f'{source}: missing source treatment or reason')
        successors=mapping.get('successorIds', [])
        expected = [source] if source in FOUNDATION_IDS else [i for i,t in new.items() if source in t.get('sourceRefs', [])]
        if not expected or successors != expected:
            errors.append(f'{source}: missing or incorrect successor mapping')
        if mapping.get('structuredPrerequisites') != originals[source]['dependsOn'] or mapping.get('textualPrerequisites') != []:
            errors.append(f'{source}: changed structured/textual prerequisite history')
        history=mapping.get('history', [])
        if len(history)!=1 or history[0].get('acceptance')!=originals[source]['acceptance'] or history[0].get('status')!=originals[source]['status']:
            errors.append(f'{source}: changed acceptance or status history')
        coverage=mapping.get('prerequisiteCoverage', [])
        if not isinstance(coverage,list) or [c.get('sourceId') for c in coverage if isinstance(c,dict)] != originals[source]['dependsOn']:
            errors.append(f'{source}: incomplete prerequisite outcome coverage'); continue
        for item in coverage:
            dep=item['sourceId']
            targets=[dep] if dep in FOUNDATION_IDS else [i for i,t in new.items() if dep in t.get('sourceRefs', [])]
            if item.get('retainedDependencyId')!=dep or item.get('successorIds')!=targets:
                errors.append(f'{source}: incorrect predecessor outcome mapping {dep}')
    if len(mapped)!=len(set(str(i) for i in mapped)) or set(mapped)!=expected_ids:
        errors.append('missing or duplicate original source mappings')


def validate(root: Path) -> tuple[list[str], int]:
    root=root.resolve(); errors: list[str]=[]
    plan=load_json(root/'plan/tasks.json', errors)
    tasks, valid=check_task_json(plan, errors) if plan else ({},False)
    if plan.get('stateAuthority')!='tasks.json' or plan.get('evidenceAuthority')!='../STATUS.md':
        errors.append('canonical stateAuthority must be tasks.json and evidenceAuthority ../STATUS.md')
    markdown=parse_task_markdown(root/'TASKS.md', errors)
    statuses=parse_status_table(root/'STATUS.md', errors)
    if tasks and valid:
        check_dependencies(tasks,errors)
        check_projection(tasks,markdown,statuses,errors)
        check_expansion(root,plan,tasks,errors)
        native={i:tasks[i] for w in plan.get('waves',[]) if isinstance(w,dict) for i in w.get('taskIds',[]) if isinstance(i,str) and i in tasks}
        check_roadmap(root,native,errors)
        if not errors:
            from render_plan import render
            for name,expected in render(plan).items():
                path=root/name
                if not path.is_file() or path.read_text(encoding='utf-8')!=expected:
                    errors.append(f'{name}: generated projection differs from canonical ledger')
    check_next_packet(root,errors)
    check_local_links(root,errors)
    return errors,len(tasks)


def main() -> int:
    errors,count=validate(parse_args().root)
    if errors:
        print(f'Vital Rehearsal plan validation FAILED ({len(errors)} issue(s)):')
        for error in errors: print('- '+error)
        return 1
    print(f'Vital Rehearsal plan validation PASS: {count} canonical records; preserved original contracts; synchronized views; mapped outcomes; acyclic dependencies and release ordering. Plan checks do not establish product or scientific completion.')
    return 0


if __name__=='__main__':
    sys.exit(main())
