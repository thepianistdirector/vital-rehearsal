"""Rights-admitted source exposure and bounded numerical experiment adapter."""
import hashlib
import importlib.resources as resources
import math

MODEL = 'bental-2006-combination'
LIMIT = ('Numerical reproduction of an unmodified historical CellML combination exposure. '
         'Not a reproduction of any single paper model, empirical validation, patient model, or clinical advice. '
         'A source pressure-derivative inconsistency is retained; normalized unit interpretation and qualified review remain pending.')
NAMES = ['V_A', 'P_A', 'f_o', 'f_c', 'p_o', 'p_c', 'z']
UNITS = ['litre', 'mmHg', 'dimensionless', 'dimensionless', 'mmHg', 'mmHg', 'dimensionless (source normalization)']

def source_hash():
    return hashlib.sha256(resources.files('vital_rehearsal').joinpath('bental_source.py').read_bytes()).hexdigest()

def card():
    return {'id': MODEL, 'admission': 'BOUNDED_NUMERICAL_REPRODUCTION_ONLY', 'limitation': LIMIT,
            'exposure': 'b503501533abcf0e70786789f08cb902', 'revision': '2e0e7ccc682bbf326829b3d78e3137ebdf8dbca0',
            'source_sha256': source_hash(), 'license': 'CC-BY-3.0',
            'source_url': 'https://models.physiomeproject.org/exposure/b503501533abcf0e70786789f08cb902/bental_2006.cellml/view',
            'states': dict(zip(NAMES, UNITS)), 'time_unit': 'second',
            'reference': 'PMR generated-code solver: scipy.integrate.ode VODE BDF, atol=rtol=1e-6, max_step=1, 500 samples 0..10 s. Same equations; no independent empirical reference.',
            'supported_domain': '0..10 seconds; source initial state; R scale 0.9..1.1 is a numerical perturbation neighbourhood, not physiological uncertainty.',
            'coupling': 'NONE: no reviewed care event or clinical delay semantics',
            'solver_methods': ['Radau','BDF','RK45','DOP853','source-vode']}

def solve(spec, directory):
    import numpy as np
    from scipy.integrate import solve_ivp, ode
    from . import bental_source as model
    import csv
    import time
    states, constants = model.initConsts()
    constants[6] *= spec['resistance_scale']
    times = np.linspace(0, spec['duration_s'], spec['samples'])
    def integrate(method, rtol, atol, step, name):
        start = time.monotonic()
        path = directory / name
        with path.open('x', newline='') as stream:
            writer = csv.writer(stream); writer.writerow(['time_s'] + NAMES)
            writer.writerow([0] + states); stream.flush()
            if method == 'source-vode':
                solver = ode(model.computeRates).set_integrator('vode', method='bdf', rtol=rtol, atol=atol, max_step=step)
                solver.set_initial_value(states, 0); solver.set_f_params(constants)
                values = [states.copy()]
                for t in times[1:]:
                    value = solver.integrate(t)
                    if not solver.successful() or not np.all(np.isfinite(value)):
                        raise ValueError('VODE unsuccessful or nonfinite; partial trajectory retained')
                    values.append(value.copy());writer.writerow([float(t)] + value.tolist());stream.flush()
                y = np.array(values).T
                nfev = None
            else:
                result = solve_ivp(lambda t,y: model.computeRates(t,y,constants), (0,float(times[-1])), states,
                                   method=method, t_eval=times, rtol=rtol, atol=atol, max_step=step)
                for t, value in zip(result.t[1:],result.y.T[1:]): writer.writerow([float(t)] + value.tolist())
                stream.flush()
                if not result.success or len(result.t) != len(times) or not np.all(np.isfinite(result.y)):
                    raise ValueError('solver incomplete or nonfinite; partial trajectory retained')
                y = result.y; nfev = result.nfev
        return y, {'wall_seconds': time.monotonic()-start, 'nfev': nfev, 'rows': len(times)}
    y, cost = integrate(spec['solver'],spec['rtol'],spec['atol'],spec['max_step_s'],'trajectory.csv')
    ref, refcost = integrate('source-vode',1e-6,1e-6,1.,'reference.csv')
    algebraic = model.computeAlgebraic(constants,y,times)
    with (directory/'algebraic.csv').open('x',newline='') as stream:
        writer=csv.writer(stream);writer.writerow(['time_s','P_L_mmHg','dP_Ldt_source_mmHg_per_s','dP_Ldt_analytic_mmHg_per_s','derivative_error_mmHg_per_s'])
        analytic = -(constants[23]*constants[1]**2*constants[2]/2)*np.cos(constants[1]*times) - constants[3]*constants[2]*constants[1]/2*np.sin(constants[1]*times)
        for i,t in enumerate(times):writer.writerow([t,algebraic[0,i],algebraic[1,i],analytic[i],algebraic[1,i]-analytic[i]])
    comparison = {name: {'unit':UNITS[i], 'max_absolute_difference':float(np.max(np.abs(y[i]-ref[i]))),
                        'rms_difference':float(np.sqrt(np.mean((y[i]-ref[i])**2))),
                        'minimum':float(np.min(y[i])), 'maximum':float(np.max(y[i])), 'final':float(y[i,-1])}
                  for i,name in enumerate(NAMES)}
    physical = bool(np.all(y[0]>0) and np.all(y[1]>47) and np.all(y[2:4]>=0) and np.all(y[2:4]<=1) and np.all(y[4:6]>=0))
    return {'execution_state':'COMPLETED','conclusion':'NUMERICAL_OUTPUT_WITH_SOURCE_WARNINGS', 'limitation':LIMIT,
            'comparison':comparison,'diagnostics':{'finite':True,'basic_state_bounds':physical,
            'source_derivative_max_abs_error_mmHg_per_s':float(np.max(np.abs(algebraic[1]-analytic))),
            'qualified_review':'PENDING','physiological_validity':'NOT_ESTABLISHED'},'cost':cost,'reference_cost':refcost}
