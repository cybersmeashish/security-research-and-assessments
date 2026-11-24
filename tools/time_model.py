"""Synthetic interval decision; a verified error bound is an external assumption."""
import math

def interval_decision(observed,uncertainty,not_before,expires,clock_verified):
    values=(observed,uncertainty,not_before,expires)
    if any(type(v) not in (int,float) or not math.isfinite(v) for v in values):raise ValueError("finite numeric values required")
    if uncertainty<0 or expires<=not_before or type(clock_verified) is not bool:raise ValueError("invalid interval or trust flag")
    if not clock_verified:return "unverified_clock"
    low=observed-uncertainty;high=observed+uncertainty
    return "allow" if low>=not_before and high<expires else "outside_or_uncertain"


def study():
    rows=[]
    for radius in (0,15,60):
        for true_time in (-30,0,15,300,570,599,600,615,660):
            for drift in (-60,-15,0,15,60):
                local=true_time+drift
                truth=0<=true_time<600
                point=0<=local<600
                bounded=interval_decision(local,radius,0,600,True)=="allow"
                rows.append({"true_time":true_time,"observed_time":local,"drift":drift,"radius":radius,
                             "bound_contains_true_time":abs(drift)<=radius,"truth_allow":truth,"point_allow":point,"interval_allow":bounded,
                             "point_unsafe_allow":point and not truth,"interval_unsafe_allow":bounded and not truth,
                             "interval_false_deny":not bounded and truth})
    return rows
