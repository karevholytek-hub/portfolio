"""Independent browser test of the isolated marketplace section; fixtures are temporary."""
import base64, json, pathlib, shutil, tempfile, threading, zipfile
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from playwright.sync_api import sync_playwright

root = pathlib.Path(__file__).resolve().parent
proof = pathlib.Path("marketplace-proof").resolve()
proof.mkdir(exist_ok=True)
png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAMAAAAECAIAAADETxJQAAAAF0lEQVR4nGPMa5rGwMDAwMDAxAAD2FgAOoQBjmIWeY0AAAAASUVORK5CYII=")
with tempfile.TemporaryDirectory() as tmp:
    base = pathlib.Path(tmp)
    target = base / "marketplace"
    shutil.copytree(root, target)
    (target / "catalog.json").write_text("[]", encoding="utf8")
    fixture = base / "sample.png"
    fixture.write_bytes(png)
    video = base / "sample.webm"
    video.write_bytes(base64.b64decode("GkXfo59ChoEBQveBAULygQRC84EIQoKEd2VibUKHgQJChYECGFOAZwEAAAAAAAOFEU2bdLpNu4tTq4QVSalmU6yBoU27i1OrhBZUrmtTrIHWTbuMU6uEElTDZ1OsggEjTbuMU6uEHFO7a1OsggNv7AEAAAAAAABZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAVSalmsCrXsYMPQkBNgIxMYXZmNjEuNy4xMDNXQYxMYXZmNjEuNy4xMDNEiYhAj0AAAAAAABZUrmvIrgEAAAAAAAA/14EBc8WI/bca9LZywm6cgQAitZyDdW5kiIEAhoVWX1ZQOIOBASPjg4QD+UCq4JCwgaC6gVqagQJVsIRVuYEBElTDZ/tzc59jwIBnyJlFo4dFTkNPREVSRIeMTGF2ZjYxLjcuMTAzc3PWY8CLY8WI/bca9LZywm5nyKFFo4dFTkNPREVSRIeUTGF2YzYxLjE5LjEwMSBsaWJ2cHhnyKFFo4hEVVJBVElPTkSHkzAwOjAwOjAxLjAwMDAwMDAwMAAfQ7Z1QcbngQCj1oEAAIDwBQCdASqgAFoAAEcIhYWIhYSIAgICdaoD+AIGmhPghqqTXcQ6qk13EOqpNdxDqqTXcQ6qk13EGAD+/00S//xYV/FhX8WFf/FhX/z8zu3F/OYAo5iBAEMAEQIABRCsABgAGFgv9AAIgIEAAACjmIEAhQARAgAFEKwAGAAYWC/0AAiAgQAAAKOYgQDIABECAAUQrAAYABhYL/QACICBAAAAo5iBAQsAEQIABRCsABgAGFgv9AAIgIEAAACjmIEBTQARAgAFEKwAGAAYWC/0AAiAgQAAAKOYgQGQABECAAUQrAAYABhYL/QACICBAAAAo5eBAdMA8QEABRAQFGAAYWC/0AAiAgQAAKOYgQIVABECAAUQrAAYABhYL/QACICBAAAAo5iBAlgAEQIABRCsABgAGFgv9AAIgIEAAACjmIECmwARAgAFEKwAGAAYWC/0AAiAgQAAAKOYgQLdABECAAUQrAAYABhYL/QACICBAAAAo5iBAyAAEQIABRCsABgAGFgv9AAIgIEAAACjmIEDYwARAgAFEKwAGAAYWC/0AAiAgQAAAKOYgQOlABECAAUQrAAYABhYL/QACICBAAAAHFO7a5G7j7OBALeK94EB8YIBo/CBAw=="))
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(SimpleHTTPRequestHandler, directory=base))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_port}/marketplace/"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(url + "?edit=1")
            page.locator("#add").click()
            page.locator("#title").fill("Тестовая карточка")
            page.locator("#desc").fill("Только тестовый материал")
            page.locator("#files").set_input_files([str(fixture)] * 29 + [str(video)])
            assert page.locator("#mediaList .media-row").count() == 30
            page.locator("#files").set_input_files(str(fixture))
            assert "Не более 30" in page.locator("#status").inner_text()
            assert page.locator("#mediaList .media-preview img").count() == 29
            assert page.locator("#mediaList .media-preview video").count() == 1
            assert page.locator("#mediaList .media-cover-label").count() == 1
            assert page.locator("#mediaList .media-row").first.locator(".media-cover-label").inner_text() == "Обложка"
            page.locator("#mediaList .media-preview img").first.scroll_into_view_if_needed()
            page.wait_for_function("document.querySelector('#mediaList img')?.naturalWidth > 0")
            page.locator("#mediaList .media-preview video").scroll_into_view_if_needed()
            page.wait_for_function("document.querySelector('#mediaList video')?.videoWidth > 0")
            page.screenshot(path=str(proof / "editor-previews-desktop.png"))
            assert page.locator("#mediaList .media-row").count() == 30
            page.locator("#save").click()
            page.locator(".card").wait_for()
            page.reload()
            page.locator(".card").wait_for()
            page.wait_for_function("document.querySelector('.cover img')?.naturalWidth > 0")
            assert "30 материалов" in page.locator("#count").inner_text()
            page.locator(".cover").click()
            assert page.locator("#thumbs button").count() == 30
            page.locator("#thumbs button").nth(29).click()
            assert "30 / 30" in page.locator("#progress").inner_text()
            v = page.locator("#large video")
            v.wait_for()
            page.wait_for_function("document.querySelector('#large video').readyState >= 2")
            assert v.evaluate("v => v.videoWidth") == 160
            v.evaluate("v => v.play()")
            page.wait_for_function("document.querySelector('#large video').currentTime > 0")
            page.screenshot(path=str(proof / "video-desktop.png"))
            page.locator("#close").click()
            page.locator("#large video").wait_for(state="detached")
            page.locator(".edit-card").click()
            assert page.locator("#mediaList .media-preview img").count() == 29
            assert page.locator("#mediaList .media-preview video").count() == 1
            page.locator("#mediaList .media-row").nth(29).get_by_role("button", name="Удалить материал").click()
            assert page.locator("#mediaList .media-row").count() == 29
            assert page.locator("#mediaList video").count() == 0
            page.locator("#cancel").click()
            page.locator(".edit-card").click()
            assert page.locator("#mediaList .media-row").count() == 30
            assert page.locator("#mediaList video").count() == 1
            page.set_viewport_size({"width": 390, "height": 900})
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#mediaList .media-row").first.scroll_into_view_if_needed()
            page.screenshot(path=str(proof / "editor-previews-mobile.png"))
            page.set_viewport_size({"width": 1440, "height": 900})
            page.locator("#mediaList .media-row").nth(29).get_by_role("button", name="Выше").click()
            page.locator("#save").click()
            page.wait_for_function("document.querySelector('#editor').hidden")
            with page.expect_download() as download:
                page.locator("#export").click()
            archive = base / "export.zip"
            download.value.save_as(str(archive))
            with zipfile.ZipFile(archive) as z:
                assert z.testzip() is None
                manifest = json.loads(z.read("catalog.json"))
                assert len(manifest[0]["media"]) == 30
                assert manifest[0]["media"][28]["kind"] == "video"
                assert len(z.namelist()) == 31
                z.extractall(target)
            context.close()
            public = browser.new_context()
            page = public.new_page()
            page.on("pageerror", lambda e: errors.append(str(e)))
            for width in [390, 768, 1440]:
                page.set_viewport_size({"width": width, "height": 900})
                page.goto(url)
                page.locator(".card").wait_for()
                assert page.locator("#editTools").is_hidden()
                assert page.locator("a[href]").count() == 0
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                page.screenshot(path=str(proof / f"gallery-{width}.png"))
                page.locator(".cover").click()
                page.locator("#next").click()
                assert "2 / 30" in page.locator("#progress").inner_text()
                page.locator("#thumbs button").nth(28).click()
                page.locator("#large video").wait_for()
                page.screenshot(path=str(proof / f"viewer-{width}.png"))
                page.keyboard.press("Escape")
                assert not page.locator("#viewer").is_visible()

            # Simulate the actual GitHub REST protocol without credentials or external writes.
            editor = browser.new_context(viewport={"width": 1440, "height": 900})
            page = editor.new_page()
            page.on("pageerror", lambda e: errors.append(str(e)))
            saved_catalog = json.loads((target / "catalog.json").read_text(encoding="utf8"))
            old_head, tree_sha, new_tree, new_head, blob_sha = "a"*40, "b"*40, "c"*40, "d"*40, "e"*40
            state = {"head": old_head, "requests": [], "manifest": None, "conflict": False, "blob_count": 0}
            def github_mock(route):
                req = route.request
                headers = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "authorization, content-type, accept, x-github-api-version", "Access-Control-Allow-Methods": "GET, POST, PATCH, OPTIONS"}
                if req.method == "OPTIONS":
                    return route.fulfill(status=204, headers=headers)
                assert req.all_headers().get("authorization") == "Bearer github_pat_test_only"
                path = req.url.split("/repos/karevholytek-hub/portfolio", 1)[1]
                state["requests"].append((req.method, path))
                body = req.post_data_json if req.method in ("POST", "PATCH") else None
                if path == "/git/ref/heads/main":
                    result = {"object":{"sha": state["head"]}}
                elif path.startswith("/contents/marketplace/catalog.json?ref="):
                    remote = saved_catalog if not state["conflict"] else []
                    result = {"encoding":"base64","content":base64.b64encode(json.dumps(remote).encode()).decode()}
                elif path == "/git/commits/"+old_head:
                    result = {"tree":{"sha":tree_sha}}
                elif path == "/git/trees/"+tree_sha+"?recursive=1":
                    result = {"truncated":False,"tree":[{"type":"blob","path":"marketplace/"+m["src"]} for c in saved_catalog for m in c["media"]]}
                elif path == "/git/blobs" and req.method == "POST":
                    assert base64.b64decode(body["content"]) == png
                    state["blob_count"] += 1
                    result = {"sha":blob_sha}
                elif path == "/git/trees" and req.method == "POST":
                    assert body["base_tree"] == tree_sha
                    assert len(body["tree"]) == 2
                    assert any(e.get("sha")==blob_sha and e["path"].startswith("marketplace/media/uploads/") for e in body["tree"])
                    state["manifest"] = json.loads(next(e["content"] for e in body["tree"] if e["path"]=="marketplace/catalog.json"))
                    result = {"sha":new_tree}
                elif path == "/git/commits" and req.method == "POST":
                    assert body["tree"] == new_tree and body["parents"] == [old_head]
                    result = {"sha":new_head}
                elif path == "/git/refs/heads/main" and req.method == "PATCH":
                    assert body == {"sha":new_head,"force":False}
                    state["head"] = new_head
                    result = {"object":{"sha":new_head}}
                else:
                    raise AssertionError((req.method,path))
                route.fulfill(status=200, json=result, headers=headers)
            page.route("https://api.github.com/**", github_mock)
            page.goto(url+"?edit=1")
            page.locator(".edit-card").click()
            page.locator("#mediaList .media-row").nth(0).get_by_role("button",name="Удалить материал").click()
            page.locator("#files").set_input_files(str(fixture))
            page.locator("#save").click()
            page.wait_for_function("document.querySelector('#editor').hidden")
            state["conflict"] = True
            page.locator("#publish").click()
            page.locator("#githubToken").fill("github_pat_test_only")
            page.locator("#publishConfirm").click()
            page.wait_for_function("document.querySelector('#publishStatus').textContent.includes('Каталог GitHub изменился')")
            assert not any(method!="GET" for method,path in state["requests"])
            page.locator("#publishCancel").click()
            state["conflict"] = False
            page.locator("#publish").click()
            page.locator("#githubToken").fill("github_pat_test_only")
            page.locator("#publishConfirm").click()
            page.wait_for_function("document.querySelector('#status').textContent.includes('Изменения отправлены в GitHub')")
            assert state["head"] == new_head and state["blob_count"] == 1
            assert len(state["manifest"][0]["media"]) == 30
            assert state["manifest"][0]["media"][0]["src"] == saved_catalog[0]["media"][1]["src"]
            assert state["manifest"][0]["media"][-1]["src"].startswith("media/uploads/")
            assert page.locator("#githubToken").input_value() == ""
            assert page.evaluate("!JSON.stringify(localStorage).includes('github_pat_test_only') && !JSON.stringify(sessionStorage).includes('github_pat_test_only')")
            page.reload()
            page.locator(".card").wait_for()
            assert page.locator(".cover img").get_attribute("src") == saved_catalog[0]["media"][1]["src"]
            editor.close()
            assert not errors, errors
            browser.close()
            print("PASS: mocked GitHub publication and conflict protection, 30-item limit, editor previews and deletion, editor persistence, reorder, video playback, ZIP CRC, published isolation, 390/768/1440 layout and viewer navigation")
    finally:
        server.shutdown()
