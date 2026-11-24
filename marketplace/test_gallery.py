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
            assert page.locator("#large video").count() == 0
            page.locator(".edit-card").click()
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
            assert not errors, errors
            browser.close()
            print("PASS: 30-item limit, editor persistence, reorder, video playback, ZIP CRC, published isolation, 390/768/1440 layout and viewer navigation")
    finally:
        server.shutdown()
