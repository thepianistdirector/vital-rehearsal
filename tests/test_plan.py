"""Mutation tests for plan invariants; no scientific validation is claimed."""
from __future__ import annotations
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import validate_plan as validator
import render_plan


class PlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=json.loads((ROOT/'plan/tasks.json').read_text())

    def plan(self):
        return copy.deepcopy(self.source)

    def errors(self, plan):
        errors=[]
        tasks,valid=validator.check_task_json(plan,errors)
        if valid:
            validator.check_dependencies(tasks,errors)
            validator.check_expansion(ROOT,plan,tasks,errors)
        return errors

    def reject(self, mutate, expected):
        plan=self.plan(); mutate(plan)
        errors=self.errors(plan)
        self.assertTrue(any(expected in e for e in errors),errors)

    def test_current_plan_and_views_are_valid(self):
        errors,count=validator.validate(ROOT)
        self.assertEqual(errors,[])
        self.assertEqual(count,len(self.source['tasks']))

    def test_duplicate_task_identity(self):
        self.reject(lambda p:p['tasks'].append(copy.deepcopy(p['tasks'][-1])), 'duplicate task id')

    def test_malformed_dependency_is_rejected_before_graph_traversal(self):
        self.reject(lambda p:p['tasks'][-1].update(dependsOn=[None]), 'dependsOn must be')

    def test_boolean_wave_is_not_an_integer(self):
        self.reject(lambda p:p['tasks'][-1].update(wave=True), 'invalid wave')

    def test_empty_owned_paths(self):
        self.reject(lambda p:p['tasks'][-1].update(ownedPaths=[]), 'ownedPaths must')

    def test_wrong_project(self):
        self.reject(lambda p:p.update(project='sibling'), 'project must')

    def test_dangling_dependency(self):
        self.reject(lambda p:p['tasks'][-1]['dependsOn'].append('VR-MISSING'), 'unknown dependency')

    def test_dependency_cycle(self):
        def mutate(p):
            p['tasks'][27]['dependsOn'].append(p['tasks'][28]['id'])
            p['tasks'][28]['dependsOn'].append(p['tasks'][27]['id'])
        self.reject(mutate,'dependency cycle')

    def test_original_acceptance_cannot_be_narrowed(self):
        self.reject(lambda p:p['tasks'][3].update(acceptance='Schema smoke is sufficient.'),'original task object changed')

    def test_original_prerequisites_cannot_be_removed(self):
        self.reject(lambda p:p['tasks'][5].update(dependsOn=[]),'original task object changed')

    def test_duplicate_outcomes(self):
        self.reject(lambda p:p['tasks'][28].update(outcome=p['tasks'][27]['outcome']),'duplicate outcome')

    def test_original_mapping_must_exist(self):
        self.reject(lambda p:p['sourceMappings'].pop(),'missing or duplicate original source mappings')

    def test_successor_mapping_must_cover_source(self):
        self.reject(lambda p:p['sourceMappings'][3].update(successorIds=[]),'successor mapping')

    def test_predecessor_outcome_coverage(self):
        self.reject(lambda p:p['sourceMappings'][5].update(prerequisiteCoverage=[]),'prerequisite outcome coverage')

    def test_unassigned_task_is_orphan(self):
        self.reject(lambda p:p['waves'][-1]['taskIds'].pop(),'orphan or duplicate historical')

    def test_task_without_foundation_path(self):
        self.reject(lambda p:p['tasks'][27].update(dependsOn=[]),'orphan task')

    def test_later_release_cannot_gate_01(self):
        self.reject(lambda p:p['tasks'][27]['dependsOn'].append(p['tasks'][-1]['id']),'later release horizon')

    def test_real_physiology_cannot_bypass_admission(self):
        def mutate(p):
            task=next(t for t in p['tasks'] if t['id']=='VR-W03-01')
            task['dependsOn'].remove('VR-W01-08')
        self.reject(mutate,'load-bearing admission/release prerequisite')

    def test_public_reproduction_cannot_precede_release(self):
        def mutate(p):
            task=next(t for t in p['tasks'] if t['id']=='VR-W05-07')
            task['dependsOn']=['VR-W05-05']
        self.reject(mutate,'load-bearing admission/release prerequisite')

    def test_wave_horizon_mismatch(self):
        self.reject(lambda p:p['waves'][1].update(targetRelease='long-term'),'release-scope mismatch')

    def test_native_wave_limit(self):
        self.reject(lambda p:p['waves'].extend(copy.deepcopy(p['waves'][:5])),'at most 32 native waves')

    def test_progress_requires_evidence(self):
        self.reject(lambda p:p['tasks'][27].update(status='DONE',evidence=[]),'non-planned status requires evidence')

    def test_unknown_source_reference(self):
        self.reject(lambda p:p['tasks'][27]['sourceRefs'].append('fabricated-source'),'unknown source reference')

    def test_textual_prerequisites_remain_separate(self):
        self.reject(lambda p:p['sourceMappings'][3].update(textualPrerequisites=['VR-F03']),'structured/textual prerequisite history')

    def test_native_export_has_no_duplicate_historical_outcomes(self):
        export=json.loads(render_plan.render(self.source)['plan/roadmap-export.json'])
        ids=[t['id'] for t in export['tasks']]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertNotIn('VR-001',ids)
        self.assertIn('VR-F01',ids)
        positions={i:n for n,i in enumerate(ids)}
        for row in export['dependencies']:
            for dependency in row['dependsOnTaskIds']:
                self.assertLess(positions[dependency],positions[row['taskId']])

    def test_projection_drift_is_rejected(self):
        errors=[]
        markdown=validator.parse_task_markdown(ROOT/'TASKS.md',errors)
        tasks={t['id']:t for t in self.source['tasks']}
        statuses=validator.parse_status_table(ROOT/'STATUS.md',errors)
        markdown['VR-W02-01']['status']='DONE'
        validator.check_projection(tasks,markdown,statuses,errors)
        self.assertTrue(any('status differs' in e for e in errors),errors)

    def test_renderer_is_pure_and_deterministic(self):
        before=copy.deepcopy(self.source)
        self.assertEqual(render_plan.render(self.source),render_plan.render(self.source))
        self.assertEqual(self.source,before)


if __name__=='__main__':
    unittest.main()
