from logging import debug
from flask import Flask, request, render_template, redirect, url_for
import math 
import numpy as np
import statsmodels.stats.power as smp


app = Flask(__name__)

@app.route("/calc-sample-size", methods=["POST", "GET"])
def calc_sample_size():
    if request.method == 'POST':
        conf_level = float(request.form['conf_level'])
        alpha = (100 - conf_level) / 100
        power_percent = float(request.form['power'])
        power = power_percent / 100
        old_cr_percent = float(request.form['old_cr'])
        old_cr = old_cr_percent / 100
        str_new_cr = request.form['new_cr']
        new_crs = [float(cr) for cr in str_new_cr.strip().split(',') if cr]
        result = {}
        

        for i in new_crs:
            result[i] = {}
            y = i / 100
            z = (100 * (y - old_cr)) / old_cr
            h = 2*math.asin(np.sqrt(old_cr)) - 2*math.asin(np.sqrt(y))
            sample_size = smp.zt_ind_solve_power(effect_size = h, alpha = alpha, power = power, alternative='two-sided') + 1
            result[i]['lift'] = round(z, 2)
            result[i]['sample_size'] = round(sample_size * 2)
            result[i]['split_size'] = round(sample_size)

    else:
        return render_template('calc-sample-size.html')
    return render_template('results.html', result=result, old_cr=old_cr_percent,
                           new_crs=str_new_cr,
                           conf_level=conf_level, power=power_percent)


@app.route("/calc-ci", methods=["POST", "GET"])
def calc_ci():
    if request.method == 'POST':
        conf_level_1 = int(request.form['conf_level_1'])
        conf_level_2 = 99 if conf_level_1 == 95 else 95
        z_score = 1.96 if conf_level_1 == 95 else 2.58

        sample_size_1 = int(request.form['sample_size_1'])
        cr_sample_1_percent = float(request.form['cr_sample_1'])
        cr_sample_1 = cr_sample_1_percent / 100

        sample_size_1_lower = cr_sample_1 - z_score * np.sqrt(
            (cr_sample_1 * (1 - cr_sample_1)) / sample_size_1)
        sample_size_1_lower = round(sample_size_1_lower * 100, 2)

        sample_size_1_upper = cr_sample_1 + z_score * np.sqrt(
            (cr_sample_1 * (1 - cr_sample_1)) / sample_size_1)
        sample_size_1_upper = round(sample_size_1_upper * 100, 2)
        is_intersection = ""

        if request.form['sample_size_2']:
            display_sample_2_block = "visible"
            sample_size_2 = int(request.form['sample_size_2'])
            cr_sample_2_percent = float(request.form['cr_sample_2'])
            cr_sample_2 = cr_sample_2_percent / 100

            sample_size_2_lower = cr_sample_2 - z_score * np.sqrt(
                (cr_sample_2 * (1 - cr_sample_2)) / sample_size_2)
            sample_size_2_lower = round(sample_size_2_lower * 100, 2)

            sample_size_2_upper = cr_sample_2 + z_score * np.sqrt(
                (cr_sample_2 * (1 - cr_sample_2)) / sample_size_2)
            sample_size_2_upper = round(sample_size_2_upper * 100, 2)

            if (cr_sample_1 > cr_sample_2):
                if (sample_size_2_upper > sample_size_1_lower):
                    is_intersection = "Доверительные интервалы пересекаются"
                    intersection_color = "red"
                else:
                    is_intersection = "Доверительные интервалы не пересекаются"
                    intersection_color = "green"

            else:
                if sample_size_1_upper > sample_size_2_lower:
                    is_intersection = "Доверительные интервалы пересекаются"
                    intersection_color = "red"
                else:
                    is_intersection = "Доверительные интервалы не пересекаются"
                    intersection_color = "green"
        else:
            sample_size_2_upper = ""
            sample_size_2_lower = ""
            sample_size_2 = ""
            cr_sample_2_percent = ""
            intersection_color = "#FFF"
            display_sample_2_block = "none"

    else:
        return render_template('calc-ci.html')
    return render_template('results_1.html',
                           sample_size_1_upper=sample_size_1_upper,
                           sample_size_1_lower=sample_size_1_lower,
                           sample_size_2_upper=sample_size_2_upper,
                           sample_size_2_lower=sample_size_2_lower,
                           sample_size_1=sample_size_1,
                           sample_size_2=sample_size_2,
                           conf_level_1=conf_level_1,
                           conf_level_2=conf_level_2,
                           cr_sample_1_percent=cr_sample_1_percent,
                           cr_sample_2_percent=cr_sample_2_percent,
                           is_intersection=is_intersection,
                           intersection_color=intersection_color,
                           display_sample_2_block=display_sample_2_block)

