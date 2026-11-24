import csv
from time_model import study

def run(root,output):
    rows=study()
    with (output/"time-study.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    summaries={}
    for radius in (0,15,60):
        subset=[x for x in rows if x["radius"]==radius]
        summaries[str(radius)]={"cases":len(subset),"invalid_bound_assumptions":sum(not x["bound_contains_true_time"] for x in subset),
            "point_unsafe_allows":sum(x["point_unsafe_allow"] for x in subset),"interval_unsafe_allows":sum(x["interval_unsafe_allow"] for x in subset),"interval_false_denies":sum(x["interval_false_deny"] for x in subset)}
    assert summaries["60"]["invalid_bound_assumptions"]==0 and summaries["60"]["interval_unsafe_allows"]==0
    return {"scope":"actual computation on a synthetic true-time/drift grid; no physical clock or NTP measurement","total_cases":len(rows),"by_radius_seconds":summaries,"assumption":"security conclusion applies only if the clock source is verified and the error bound contains actual true time"}
