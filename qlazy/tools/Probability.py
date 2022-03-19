# -*- coding: utf-8 -*-
""" functions related to probability """
import math

import qlazy.config as cfg

def freq2prob(freq):
    """
    frequency to probability

    Arguments
    ----------
    freq : instance of Counter
        frequency data
        ex) Counter({'00': 53, '11': 47})

    Returns
    -------
    prob : dict
        probability data
        ex) {'00': 0.53, '11': 0.47}

    """
    total = sum(freq.values())
    prob = {k: v/total for k, v in freq.items()}
    return prob

def entropy(prob):
    """
    entropy

    Arguments
    ----------
    prob : dict
        probability data
        ex) {'00': 0.53, '11': 0.47}

    Returns
    -------
    value : float
        entropy, sum of -prob[i] log(prob[i])

    """
    if abs(sum(prob.values()) - 1.0) > cfg.EPS:
        raise ValueError("sum of probabilities is not 1.0")

    value = 0.0
    for v in prob.values():
        if v == 0.0:
            continue
        value -= v * math.log2(v)

    return value

def kl_divergence(prob_0, prob_1):
    """
    KL divergence

    Arguments
    ----------
    prob_0 : dict
        probability data
        ex) {'00': 0.53, '11': 0.47}

    prob_1 : dict
        probability data
        ex) {'00': 0.51, '11': 0.49}

    Returns
    -------
    value : float
        KL divergence, sum of prob_0[i] log(prob_0[i] / prob_1[i])

    """
    if ((abs(sum(prob_0.values()) - 1.0) > cfg.EPS or
         abs(sum(prob_1.values()) - 1.0) > cfg.EPS)):
        raise ValueError("sum of probabilities is not 1.0")

    value = 0.0
    for k, v in prob_0.items():
        if v < 0.0:
            raise ValueError("probability must be positive.")
        if v > 1.0:
            raise ValueError("probability must be less than 1.")
        if v == 0.0:
            continue
        if v > 0.0:
            if k not in prob_1.keys() or prob_1[k] == 0.0:
                value = float('inf')
                break
        value += (v * math.log2(v / prob_1[k]))

    return value

def cross_entropy(prob_0, prob_1):
    """
    cross entropy

    Arguments
    ----------
    prob_0 : dict
        probability data
        ex) {'00': 0.53, '11': 0.47}

    prob_1 : dict
        probability data
        ex) {'00': 0.51, '11': 0.49}

    Returns
    -------
    value : float
        cross entropy, sum of -prob_0[i] log(prob_1[i])

    """
    if ((abs(sum(prob_0.values()) - 1.0) > cfg.EPS or
         abs(sum(prob_1.values()) - 1.0) > cfg.EPS)):
        raise ValueError("sum of probabilities is not 1.0")

    value = 0.0
    for k, v in prob_0.items():
        if v == 0.0:
            continue
        if k not in prob_1.keys():
            continue
        if prob_1[k] == 0.0:
            continue
        value -= v * math.log2(prob_1[k])

    return value
