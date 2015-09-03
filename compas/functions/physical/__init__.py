#-*- coding: utf-8 -*-
#
# Copyright 2015 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl

"""
Contains a comprehensive list of all functions/formulas within CO2MPAS.

Docstrings should provide sufficient understanding for any individual function.

Modules:

.. currentmodule:: compas.functions.physical

.. autosummary::
    :nosignatures:
    :toctree: physical/

    vehicle
    wheels
    final_drive
    gear_box
    torque_converter
    engine
    utils
    constants

"""

__author__ = 'Vincenzo Arcidiacono'

from heapq import heappush
from sklearn.metrics import mean_absolute_error
from compas.dispatcher import Dispatcher
from compas.dispatcher.utils import heap_flush
import numpy as np
from itertools import zip_longest, chain
from compas.functions.physical.engine.co2_emission import calibrate_model_params


def compare_result(target_ids, model_results, target_results, sample_weight=()):

    err, weights = [], []
    to_list = lambda *args: [np.asarray(v, dtype=float) for v in args]
    for t, w in zip_longest(target_ids, sample_weight, fillvalue=1):
        if t in model_results and t in target_results:
            y = (target_results[t], model_results[t])

            e = mean_absolute_error(*[to_list(x) for x in y])
            err.append(e)
            weights.append(w)

    return np.average(err, weights=weights) if err else np.nan


def comparison_model():
    models = [{
        'models': ('max_gear',),
        'targets': (),
    }]

    dsp = Dispatcher()

    from compas.models.physical.engine import engine
    # engine_temperature_regression_model
    dsp.add_dispatcher(
        dsp_id='test engine_temperature_regression_model',
        dsp=engine(),
        inputs={
            'engine_temperature_regression_model':
                'engine_temperature_regression_model',
            'gear_box_powers_in': 'gear_box_powers_in',
            'gear_box_speeds_in': 'gear_box_speeds_in',
            'initial_temperature': 'initial_engine_temperature'
        },
        outputs={
            'engine_temperatures': 'engine_temperatures'
        }
    )

    models.append({
        'models': ('engine_temperature_regression_model',),
        'targets': ('engine_temperatures',)
    })

    # start_stop_model
    dsp.add_dispatcher(
        dsp_id='test start_stop_model',
        dsp=engine(),
        inputs={
            'start_stop_model': 'start_stop_model',
            'times': 'times',
            'velocities': 'velocities',
            'accelerations': 'accelerations',
            'engine_temperatures': 'engine_temperatures',
            'cycle_type': 'cycle_type',
            'gear_box_type': 'gear_box_type'
        },
        outputs={
            'on_engine': 'on_engine',
            'engine_starts': 'engine_starts'
        }
    )

    models.append({
        'models': ('start_stop_model',),
        'targets': ('on_engine',)
    })

    # cold_start_speed_model
    dsp.add_dispatcher(
        dsp_id='test cold_start_speed_model',
        dsp=engine(),
        inputs={
            'gear_box_speeds_in': 'gear_box_speeds_in',
            'on_engine': 'on_engine',
            'idle_engine_speed': 'idle_engine_speed',
            'engine_temperatures': 'engine_temperatures',
            'engine_thermostat_temperature': 'engine_thermostat_temperature',
            'cold_start_speed_model': 'cold_start_speed_model'
        },
        outputs={
            'engine_speeds_out': 'engine_speeds_out'
        }
    )

    models.append({
        'models': ('cold_start_speed_model', 'idle_engine_speed',
                   'engine_thermostat_temperature'),
        'targets': ('engine_speeds_out',)
    })

    # co2_params
    from compas.models.physical.engine.co2_emission import co2_emission
    dsp.add_dispatcher(
        dsp_id='test co2_params',
        dsp=co2_emission(),
        inputs={
            'co2_emissions_model': 'co2_emissions_model',
            'co2_params': 'co2_params'
        },
        outputs={
            'co2_emissions': 'co2_emissions'
        }
    )

    models.append({
        'models': ('co2_params',),
        'targets': ('co2_emissions',)
    })

    # calibration of all
    dsp.add_dispatcher(
        dsp_id='calibration_co2_params_with_all_calibration_cycles',
        dsp=co2_emission(),
        inputs={
            'co2_emissions_model': 'co2_emissions_model',
            'co2_params': 'co2_params'
        },
        outputs={
            'co2_emissions': 'co2_emissions'
        }
    )

    def calibrate_co2_params_with_all_calibration_cycles(
            extracted_models, *calibration_outputs):
        if len(calibration_outputs) <= 1:
            return
        co = calibration_outputs

        c_name = extracted_models['origin calibrated_models']
        c_name = c_name['engine_temperature_regression_model']

        def check(data):
            return 'co2_params_initial_guess' in data and 'co2_params_bounds' in data

        its = [(o for o in co if o['cycle_name'] == c_name and check(o)),
                (o for o in co if check(o))]

        data = {}
        for it in its:
            data = next(it, {})
            if data:
                break

        if not data:
            return

        initial_guess = data['co2_params_initial_guess']
        bounds = data['co2_params_bounds']

        e_tag = 'co2_error_function'
        error_function = [o[e_tag] for o in co if e_tag in o]

        p = calibrate_model_params(bounds, error_function, initial_guess)
        return {'co2_params': p}

    models.append({
        'models': ('co2_params',),
        'targets': ('co2_emissions',),
        'post_processing': calibrate_co2_params_with_all_calibration_cycles
    })

    # alternator_status_model
    from compas.models.physical.electrics import electrics
    dsp.add_dispatcher(
        dsp_id='test alternator_status_model',
        dsp=electrics(),
        inputs={
            'battery_capacity': 'battery_capacity',
            'alternator_status_model': 'alternator_status_model',
            'alternator_charging_currents': 'alternator_charging_currents',
            'max_battery_charging_current': 'max_battery_charging_current',
            'alternator_nominal_voltage': 'alternator_nominal_voltage',
            'start_demand': 'start_demand',
            'electric_load': 'electric_load',
            'initial_state_of_charge': 'initial_state_of_charge',
            'times': 'times',
            'gear_box_powers_in': 'gear_box_powers_in',
            'on_engine': 'on_engine',
            'engine_starts': 'engine_starts'
        },
        outputs={
            'alternator_currents': 'alternator_currents',
            'battery_currents': 'battery_currents',
            'state_of_charges': 'state_of_charges',
            'alternator_statuses': 'alternator_statuses'
        }
    )

    models.append({
        'models': ('alternator_charging_currents', 'start_demand',
                   'max_battery_charging_current', 'electric_load',
                   'alternator_status_model'),
        'targets': ('alternator_currents', 'battery_currents')
    })

    # AT_gear
    from compas.models.physical.gear_box.AT_gear import AT_gear

    at = AT_gear()

    dsp.add_from_lists(
        data_list=[{'data_id': k, 'default_value': v}
                   for k, v in at.default_values.items()]
    )

    dsp.add_dispatcher(
        dsp_id='test AT_gear',
        dsp=at,
        inputs={
            'correct_gear': 'correct_gear',
            'CMV': 'CMV',
            'CMV_Cold_Hot': 'CMV_Cold_Hot',
            'DT_VA': 'DT_VA',
            'DT_VAT': 'DT_VAT',
            'DT_VAP': 'DT_VAP',
            'DT_VATP': 'DT_VATP',
            'GSPV': 'GSPV',
            'GSPV_Cold_Hot': 'GSPV_Cold_Hot',
            'accelerations': 'accelerations',
            'gear_box_powers_out': 'gear_box_powers_out',
            'engine_temperatures': 'engine_temperatures',
            'time_cold_hot_transition': 'time_cold_hot_transition',
            'times': 'times',
            'velocities': 'velocities',
        },
        outputs={
            'gears': 'gears',
        }
    )

    def AT_get_inputs(extracted_models, *args, **kwargs):
        i = get_inputs(extracted_models, *args)
        k = i['AT_gear_shifting_model'][0]
        i[k] = extracted_models[k]
        return i

    models.append({
        'models': ('AT_gear_shifting_model', 'correct_gear',
                   'upper_bound_engine_speed'),
        'targets': ('gears',),
        'get_inputs': AT_get_inputs
    })

    return dsp, models


def get_inputs(extracted_models, outputs, models, targets, **kwargs):
    inputs = {k: v for k, v in outputs.items() if k not in targets}
    inputs.update({m: extracted_models[m] for m in models})
    return inputs


def model_selector(*calibration_outputs):
    """
    Selects the best calibrated models from many sources (e.g., WLTP, WLTP-L).

    :param calibration_outputs:
        A tuple of dictionaries that have all calibration cycle outputs.
    :type calibration_outputs: (dict, ...)

    :return:
        The best calibrated models.
    :rtype: dict
    """

    co = calibration_outputs
    models = {}
    models['origin calibrated_models'] = origin = {}
    dsp, _model_targets = comparison_model()

    # get calibrated models and data for comparison
    m = set(chain.from_iterable(m['models'] for m in _model_targets))
    id_tag = 'cycle_name'
    get = lambda i, o: (get_models(o, m), co[:i] + co[i + 1:], o[id_tag])
    em_rt = list(map(get, range(len(co)), co))

    for d in _model_targets:
        heap, mods, trgs = [], d['models'], d['targets']
        get_i = d.get('get_inputs', get_inputs)
        post = d.get('post_processing', lambda *args: None)

        def error_fun(e_mods, res_t, co_i):
            if any(m not in e_mods for m in mods):
                return
            err = []
            for t in res_t:
                if all(k not in t for k in trgs):
                    continue
                pred = dsp.dispatch(get_i(e_mods, t, **d), trgs, shrink=True)[1]
                err.append(compare_result(trgs, pred, t))

            m = {k: e_mods[k] for k in mods if k in e_mods}
            err = np.mean(err) if err else np.nan
            heappush(heap, (err, len(e_mods), co_i, m))

        for v in em_rt:
            error_fun(*v)

        e_mods = post(models, *co)
        if e_mods:
            error_fun(e_mods, co, 'ALL')

        if heap:
            models.update(heap[0][-1])
            rank = [(v[-2], v[0]) for v in heap_flush(heap)]
            origin.update(dict.fromkeys(mods, rank[0][0]))
            print('Models %s are selected from %s (%.3f) respect to targets %s.'
                  '\nErrors %s.' % (mods, rank[0][0], rank[0][1], trgs, rank))


    return models


def get_models(calibration_outputs, models_to_extract):
    calibration_outputs = calibration_outputs
    models = {}

    for k in models_to_extract:
        if k in calibration_outputs:
            models[k] = calibration_outputs[k]

    # A/T gear shifting
    methods_ids = {
        'CMV_error_coefficients': 'CMV',
        'CMV_Cold_Hot_error_coefficients': 'CMV_Cold_Hot',
        'GSPV_error_coefficients': 'GSPV',
        'GSPV_Cold_Hot_error_coefficients': 'GSPV_Cold_Hot',
        'DT_VA_error_coefficients': 'DT_VA',
        'DT_VAT_error_coefficients': 'DT_VAT',
        'DT_VAP_error_coefficients': 'DT_VAP',
        'DT_VATP_error_coefficients': 'DT_VATP',
    }

    m = []

    for e, k in methods_ids.items():
        e = calibration_outputs.get(e, None)
        if e:
            e = (e['mean_absolute_error'], e['correlation_coefficient'])
            heappush(m, (e[0] / e[1], e, k))
    if m:
        e, k = m[0][1:]

        models[k] = calibration_outputs[k]
        models['AT_gear_shifting_model'] = (k, e)

        print('AT_gear_shifting_model: %s with mean_absolute_error %.3f [RPM] '
              'and correlation_coefficient %.3f' % (k, e[0], e[1]))

    return models
