from logging import debug
from flask import Flask, request, render_template, redirect, url_for
import math 
import numpy as np
import statsmodels.stats.power as smp


app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == 'POST':
        alpha = float(request.form['alpha'])
        power = float(request.form['power'])
        old_cr = float(request.form['old_cr'])
        str_new_cr = request.form['new_cr'].strip()
        new_crs = [float(cr) for cr in str_new_cr.split(',') if cr]
        result = {}
        

        for i in new_crs:
            result[i] = {}
            y = i
            z = (100 * (y - old_cr)) / old_cr
            h = 2*math.asin(np.sqrt(old_cr)) - 2*math.asin(np.sqrt(y))
            sample_size = smp.zt_ind_solve_power(effect_size = h, alpha = alpha, power = power, alternative='two-sided') + 1
            result[i]['lift'] = round(z, 2)
            result[i]['sample_size'] = round(sample_size * 2)
            result[i]['split_size'] = round(sample_size)

    else:
        return render_template('calculate.html')
    return render_template('results.html', result=result, old_cr=old_cr)
    
