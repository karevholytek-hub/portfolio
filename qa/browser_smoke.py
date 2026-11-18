#!/usr/bin/env python3
"""HTTP Chromium smoke; screenshots aren't artistic approval or real Android proof."""
import argparse
import functools
import json
import socketserver
import threading
from pathlib import Path
from http.server import SimpleHTTPRequestHandler

from playwright.sync_api import sync_playwright


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass


def run(site,out):
    site=Path(site).resolve(); out=Path(out).resolve(); out.mkdir(exist_ok=True,parents=True)
    if not (site/"index.html").exists():
        print("Missing index.html"); return 1
    handler=functools.partial(QuietHandler,directory=str(site))
    results=[]
    with socketserver.TCPServer(("127.0.0.1",0),handler) as server:
        thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start()
        url="http://127.0.0.1:%d/" % server.server_address[1]
        try:
            with sync_playwright() as p:
                browser=p.chromium.launch(headless=True)
                for width,height in [(390,844),(768,1024),(1440,900)]:
                    page=browser.new_page(viewport={"width":width,"height":height},
                        is_mobile=(width==390),has_touch=(width==390),device_scale_factor=1)
                    errors=[]; page.on("pageerror",lambda e: errors.append(str(e)))
                    try:
                        r=page.goto(url,wait_until="domcontentloaded",timeout=20000)
                        page.wait_for_function("() => window.__lumScene && window.__lumScene.ready",timeout=20000)
                        page.wait_for_timeout(900)
                        motion_before=page.evaluate("""() => ({
                            flower:getComputedStyle(document.querySelector('#flower-sway')).transform,
                            nature:getComputedStyle(document.querySelector('#nature-0')).transform
                        })""")
                        page.wait_for_timeout(850)
                        motion_after=page.evaluate("""() => ({
                            flower:getComputedStyle(document.querySelector('#flower-sway')).transform,
                            nature:getComputedStyle(document.querySelector('#nature-0')).transform
                        })""")
                        data=page.evaluate("""() => ({
                            width:innerWidth,
                            scrollWidth:document.documentElement.scrollWidth,
                            title:document.title,
                            links:document.querySelectorAll('a[href]').length,
                            cat:!!document.querySelector('#catCanvas,[data-cat-rig]'),
                            sceneReady:!!window.__lumScene?.ready,
                            decoded:window.__lumScene?.decoded,
                            expectedDecoded:window.__lumScene?.assets,
                            failedAssets:window.__lumScene?.failed,
                            natureObjects:document.querySelectorAll('.nature-object').length,
                            seedCount:document.querySelectorAll('.seed-particle').length,
                            canopyForward:[...document.querySelectorAll('.seed-particle svg')].every(
                                svg=>getComputedStyle(svg).transform.startsWith('matrix(-1,')),
                            brokenLocalImages:[...document.images].filter(img=>
                              (img.loading!=='lazy'||img.getBoundingClientRect().top < innerHeight*2)
                              && (!img.complete||img.naturalWidth===0))
                              .filter(img=>{try{return new URL(img.src).origin===location.origin}catch{return true}})
                              .map(img=>img.getAttribute('src'))
                        })""")
                        if data["cat"]:
                            page.mouse.move(int(width*.75),int(height*.3))
                            if page.locator("#catPlay").count():
                                page.locator("#catPlay").click(timeout=5000)
                                page.wait_for_timeout(600)
                        page.screenshot(path=str(out/("screen-%d.png"%width)),full_page=True)
                        issues=[]
                        if r is None or r.status>=400: issues.append("HTTP error")
                        if data["scrollWidth"]>width+2: issues.append("horizontal overflow")
                        if not data["title"].strip(): issues.append("empty title")
                        if not data["links"]: issues.append("no navigation")
                        if data["brokenLocalImages"]: issues.append("broken local images")
                        if not data["sceneReady"] or data["decoded"]!=data["expectedDecoded"] or data["failedAssets"]:
                            issues.append("photographic scene failed to decode atomically")
                        if data["natureObjects"]<5: issues.append("nature layers missing")
                        if data["seedCount"]==0 or not data["canopyForward"]: issues.append("seed drift/orientation failed")
                        if motion_before["flower"]==motion_after["flower"]: issues.append("main dandelion is static")
                        if motion_before["nature"]==motion_after["nature"]: issues.append("surrounding plants are static")
                        if errors: issues.append("JavaScript runtime error(s)")
                        results.append({"width":width,"status":"FAIL" if issues else "TECHNICAL_PASS",
                                        "issues":issues,"metrics":data,"page_errors":errors,
                                        "motion_before":motion_before,"motion_after":motion_after})
                    except Exception as e:
                        results.append({"width":width,"status":"FAIL","issues":[str(e)]})
                    finally: page.close()
                browser.close()
        finally:
            server.shutdown()
    (out/"report.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf8")
    for item in results:
        print(item["width"],item["status"],"; ".join(item["issues"]))
    return 1 if any(x["status"]=="FAIL" for x in results) else 0


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--site",default=".")
    parser.add_argument("--out",default="qa-artifacts")
    opts=parser.parse_args()
    raise SystemExit(run(opts.site,opts.out))
