from pathlib import Path
import argparse,datetime,hashlib,io,json,os,platform,re,socket,sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))


def verify(output,isolated=False):
    output.mkdir(parents=True,exist_ok=True)
    suite=unittest.defaultTestLoader.discover(str(ROOT/"tests"));count=suite.countTestCases();log=io.StringIO()
    result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
    (output/"tests.log").write_text(log.getvalue())
    if not result.wasSuccessful():raise AssertionError(log.getvalue())
    from experiment import run
    observations=run(ROOT,output)
    (output/"results.json").write_text(json.dumps(observations,indent=2,allow_nan=False)+"\n")
    (output/"verification.json").write_text(json.dumps({"verification_in_progress":True})+"\n")
    links=0
    for path in ROOT.rglob("*.md"):
        if "evidence" in path.relative_to(ROOT).parts:continue
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)",path.read_text()):
            if target.startswith(("https://","http://","#","mailto:")):continue
            if not (path.parent/target.split("#")[0]).resolve().exists():raise AssertionError("Broken local link: "+str(path)+": "+target)
            links+=1
    files=[p for p in ROOT.rglob("*") if p.is_file() and "evidence" not in p.relative_to(ROOT).parts and "__pycache__" not in p.parts and p.suffix!=".pyc"]
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
    (output/"source-manifest.json").write_text(json.dumps(hashes,indent=2)+"\n")
    network={"requested":isolated}
    if isolated:
        names=sorted(p.name for p in Path("/sys/class/net").iterdir())
        with socket.socket() as s:
            s.settimeout(1)
            try:s.connect(("198.51.100.1",443));network["probe"]="unexpected_connection"
            except OSError as e:network.update({"probe":"blocked","errno":e.errno,"exception":type(e).__name__})
        routes=Path("/proc/net/route").read_text().splitlines()[1:]
        default=any(line.split()[1]=="00000000" for line in routes if len(line.split())>1)
        network.update({"interfaces":names,"default_ipv4_route":default,"root_read_only":bool(os.statvfs("/").f_flag & os.ST_RDONLY),"workspace_read_only":bool(os.statvfs(str(ROOT)).f_flag & os.ST_RDONLY),"uid":os.getuid()})
        assert names==["lo"] and not default and network.get("errno")==101 and network["workspace_read_only"]
    record={"executed_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"runtime":{"python":platform.python_version(),"system":platform.system(),"machine":platform.machine()},
            "unique_regression_tests":count,"source_manifest_files":len(hashes),"local_links_checked":links,"isolation":network,
            "contribution":json.loads((ROOT/"fixtures/contribution.json").read_text()),"experiment_scope":observations.get("scope"),"stage":"local contribution evidence; no customer or vendor outcome claim"}
    (output/"verification.json").write_text(json.dumps(record,indent=2)+"\n")
    print(json.dumps({"repository":record["contribution"]["slug"],"tests":count,"links":links,"source_files":len(hashes),"isolated":isolated,"observations":observations},indent=2))
    return record

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True);p.add_argument("--isolated",action="store_true");a=p.parse_args();verify(a.output,a.isolated)
