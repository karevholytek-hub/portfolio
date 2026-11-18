#!/usr/bin/env python3
"""Fail closed on PR/push changes to the live UI unless G01..G08 release gate passes."""
import argparse
import subprocess
import sys
from pathlib import Path


def is_public_visual(path):
    path=path.replace("\\","/")
    if path == "index.html": return True
    if path.startswith(("assets/","css/","js/","images/","media/","public/")): return True
    if path.endswith((".html",".css",".js",".jsx",".tsx",".webp",".png",".jpg",".jpeg",".svg",".gif",".avif",".mp4",".webm")):
        return not path.startswith(("qa/","tests/",".github/","docs/"))
    return False


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--base",default="origin/main")
    parser.add_argument("--mode",choices=["pull_request","push","workflow_dispatch"],default="pull_request")
    parser.add_argument("--gh-output",default=None)
    opts=parser.parse_args()
    def set_output(value):
        if opts.gh_output:
            with open(opts.gh_output,"a",encoding="utf-8") as f:
                f.write("visual_changed="+str(value).lower()+"\\n")
    if opts.mode == "workflow_dispatch":
        set_output(False)
        print("Manual dispatch: strict gate is controlled separately.")
        return 0
    if not opts.base or set(opts.base)=={"0"}:
        print("FAIL: no reliable base commit to compare")
        return 1
    diff_args=["git","diff","--name-only"]
    if opts.mode=="pull_request": diff_args.append(opts.base+"...HEAD")
    else: diff_args.extend([opts.base,"HEAD"])
    cmd=subprocess.run(diff_args,text=True,capture_output=True)
    if cmd.returncode:
        print("FAIL: cannot determine changed files",cmd.stderr)
        return 1
    files=[p.strip() for p in cmd.stdout.splitlines() if p.strip()]
    visual=[p for p in files if is_public_visual(p)]
    if not visual:
        set_output(False)
        print("Non-public QA/documentation changes only; technical preflight still required.")
        return 0
    set_output(True)
    print("Public visuals changed; require full evidence-based acceptance:",", ".join(visual))
    script=Path(__file__).resolve().parent/"check_release.py"
    return subprocess.call([sys.executable,str(script),"--mode","release"])


if __name__=="__main__":
    raise SystemExit(main())
