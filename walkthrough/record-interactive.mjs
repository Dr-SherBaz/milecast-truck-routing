/**
 * Interactive Milecast walkthrough recorder.
 * Human-ish cursor: variable speed, overshoot, pauses, circles, slider drag.
 */
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT_DIR = path.join(__dirname, "playwright-video");
const FINAL = path.join(__dirname, "Milecast-Interactive-Walkthrough.mp4");
const APP = process.env.MILECAST_URL || "http://127.0.0.1:3000";

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const rand = (a, b) => a + Math.random() * (b - a);

async function humanMove(page, x, y, { steps } = {}) {
  const n = steps ?? Math.floor(rand(18, 42));
  await page.mouse.move(x, y, { steps: n });
  if (Math.random() < 0.35) await sleep(rand(120, 380));
}

async function wobble(page, x, y) {
  await humanMove(page, x + rand(-10, 10), y + rand(-8, 8), { steps: 8 });
  await humanMove(page, x + rand(-6, 6), y + rand(-6, 6), { steps: 6 });
  await humanMove(page, x, y, { steps: 5 });
}

async function circle(page, x, y, r = 28) {
  const pts = 16;
  for (let i = 0; i <= pts; i++) {
    const a = (i / pts) * Math.PI * 2;
    await page.mouse.move(x + Math.cos(a) * r, y + Math.sin(a) * r, { steps: 2 });
  }
  await humanMove(page, x, y, { steps: 6 });
}

async function injectCursor(page) {
  await page.addStyleTag({
    content: `
      html, body, * { cursor: none !important; }
      #milecast-cursor {
        position: fixed; z-index: 2147483647; width: 28px; height: 28px;
        left: 0; top: 0; pointer-events: none;
        transform: translate(0, 0);
        filter: drop-shadow(1px 1px 1px rgba(0,0,0,.35));
      }
      #milecast-cursor svg { display: block; width: 28px; height: 28px; }
      #milecast-cursor.down { transform: scale(0.92); transform-origin: 2px 2px; }
      #milecast-cursor-label {
        position: fixed; z-index: 2147483647; pointer-events: none;
        font: 600 12px/1.2 "Segoe UI", sans-serif; color: #13202c;
        background: rgba(255,255,255,.92); border: 1px solid #c9d3db;
        padding: 4px 8px; border-radius: 4px; opacity: 0; transition: opacity .2s;
      }
      #milecast-cursor-label.on { opacity: 1; }
    `,
  });
  await page.evaluate(() => {
    const c = document.createElement("div");
    c.id = "milecast-cursor";
    // Classic OS arrow pointer (tip at top-left)
    c.innerHTML = `
      <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <path d="M4 2 L4 18 L8.2 14.3 L11.2 21.5 L13.6 20.5 L10.5 13.2 L16 13 Z"
          fill="#000" stroke="#fff" stroke-width="1.4" stroke-linejoin="round"/>
      </svg>`;
    const lab = document.createElement("div");
    lab.id = "milecast-cursor-label";
    document.body.append(c, lab);
    window.__mcCursor = (x, y, down) => {
      c.style.left = `${x}px`;
      c.style.top = `${y}px`;
      c.classList.toggle("down", !!down);
      lab.style.left = `${x + 20}px`;
      lab.style.top = `${y + 20}px`;
    };
    window.__mcLabel = (text) => {
      lab.textContent = text || "";
      lab.classList.toggle("on", !!text);
    };
    window.addEventListener(
      "mousemove",
      (e) => window.__mcCursor(e.clientX, e.clientY, e.buttons === 1),
      true,
    );
  });
}

async function label(page, text, ms = 1800) {
  await page.evaluate((t) => window.__mcLabel(t), text);
  await sleep(ms);
  await page.evaluate(() => window.__mcLabel(""));
}

async function boxCenter(locator) {
  const box = await locator.boundingBox();
  if (!box) throw new Error("missing box");
  return { x: box.x + box.width / 2, y: box.y + box.height / 2, box };
}

async function main() {
  const browser = await chromium.launch({
    headless: true,
    args: ["--window-size=1440,900"],
  });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    recordVideo: { dir: OUT_DIR, size: { width: 1440, height: 900 } },
  });
  const page = await context.newPage();
  await page.goto(APP, { waitUntil: "networkidle", timeout: 60000 });
  await injectCursor(page);
  await sleep(2800);

  // Brand / intro gestures — room to talk
  await humanMove(page, 80, 60, { steps: 40 });
  await sleep(900);
  await circle(page, 90, 70, 22);
  await label(page, "Milecast", 3200);
  await sleep(rand(1400, 2000));
  await humanMove(page, 420, 160, { steps: 48 });
  await wobble(page, 420, 160);
  await label(page, "what this app does", 3500);
  await sleep(1600);
  await humanMove(page, 1180, 55, { steps: 50 });
  await circle(page, 1180, 55, 18);
  await label(page, "React + Django", 3000);
  await sleep(1800);

  // Form fields
  const origin = page.getByLabel("Origin");
  const dest = page.getByLabel("Destination");
  const weight = page.getByLabel(/Load weight/i);
  const spacing = page.getByLabel(/Checkpoint spacing/i);
  const slider = page.locator("#forecast");
  const build = page.getByRole("button", { name: /Build weather-aware plan/i });

  let p = await boxCenter(origin);
  await humanMove(page, p.x - 40, p.y - 30, { steps: 22 });
  await humanMove(page, p.x, p.y, { steps: 14 });
  await page.mouse.click(p.x, p.y);
  await label(page, "origin", 2200);
  await origin.fill("");
  await origin.type("Denver, CO", { delay: rand(70, 120) });
  await sleep(1400);

  p = await boxCenter(dest);
  await humanMove(page, p.x + rand(-20, 40), p.y - 20, { steps: 34 });
  await sleep(500);
  await humanMove(page, p.x, p.y, { steps: 14 });
  await page.mouse.click(p.x, p.y);
  await label(page, "destination", 2000);
  await dest.fill("");
  await dest.type("Kansas City, MO", { delay: rand(65, 110) });
  await sleep(1200);

  p = await boxCenter(weight);
  await humanMove(page, p.x, p.y, { steps: 30 });
  await page.mouse.click(p.x, p.y);
  await label(page, "load weight", 2400);
  await weight.fill("");
  await weight.type("28000", { delay: 95 });
  await sleep(1500);

  p = await boxCenter(spacing);
  await humanMove(page, p.x, p.y, { steps: 26 });
  await page.mouse.click(p.x, p.y);
  await sleep(700);
  await spacing.selectOption("50");
  await label(page, "every 50 miles", 2600);
  await sleep(1200);

  // Risk rules panel — wander down list
  await humanMove(page, 1100, 280, { steps: 42 });
  await label(page, "PDF risk rules", 2800);
  for (const y of [320, 370, 420, 470, 520]) {
    await humanMove(page, 1080 + rand(-30, 30), y, { steps: Math.floor(rand(18, 34)) });
    await sleep(rand(700, 1200));
  }
  await circle(page, 1100, 480, 26);
  await label(page, "heavy load + wind", 3200);
  await sleep(1600);

  // Slider: drag with uneven path
  p = await boxCenter(slider);
  const box = p.box;
  const startX = box.x + 8;
  const endX = box.x + box.width * 0.55;
  const midY = box.y + box.height / 2;
  await humanMove(page, startX - 30, midY - 40, { steps: 20 });
  await humanMove(page, startX, midY, { steps: 10 });
  await label(page, "0–48h forecast slider", 3000);
  await sleep(1000);
  await page.mouse.move(startX, midY);
  await page.mouse.down();
  await page.evaluate(() => {
    const c = document.getElementById("milecast-cursor");
    if (c) c.classList.add("down");
  });
  // uneven drag — slow then faster
  const pathPts = [];
  for (let i = 1; i <= 28; i++) {
    const t = i / 28;
    const ease = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
    pathPts.push({
      x: startX + (endX - startX) * ease + rand(-2, 2),
      y: midY + Math.sin(t * Math.PI * 3) * rand(0, 3),
    });
  }
  for (const pt of pathPts) {
    await page.mouse.move(pt.x, pt.y, { steps: Math.floor(rand(2, 6)) });
    await sleep(rand(40, 110));
  }
  await page.mouse.up();
  await page.evaluate(() => {
    const c = document.getElementById("milecast-cursor");
    if (c) c.classList.remove("down");
  });
  await label(page, "drag to shift forecast window", 3200);
  await sleep(1400);
  // drag back toward 0 for clean plan
  await page.mouse.move(endX, midY, { steps: 10 });
  await page.mouse.down();
  await page.mouse.move(startX + 4, midY, { steps: 36 });
  await page.mouse.up();
  await sleep(1600);

  // Build
  p = await boxCenter(build);
  await humanMove(page, p.x - 50, p.y + 30, { steps: 24 });
  await sleep(700);
  await humanMove(page, p.x, p.y, { steps: 28 });
  await wobble(page, p.x, p.y);
  await label(page, "build the plan…", 2800);
  await sleep(900);

  const planWait = page.waitForResponse(
    (res) => res.url().includes("/api/plan") && res.request().method() === "POST",
    { timeout: 120000 },
  );
  await page.mouse.click(p.x, p.y);
  let planOk = false;
  try {
    const res = await planWait;
    planOk = res.ok();
    console.log("plan status", res.status());
  } catch (err) {
    console.log("plan wait failed", String(err));
  }

  // Idle micro-moves while UI paints
  const results = page.getByRole("heading", { name: /Three routes/i });
  const errBox = page.locator(".error, [role='alert']");
  const started = Date.now();
  while (Date.now() - started < 45000) {
    if (await results.isVisible().catch(() => false)) {
      planOk = true;
      break;
    }
    if (await errBox.isVisible().catch(() => false)) {
      console.log("UI error:", await errBox.innerText().catch(() => ""));
      break;
    }
    await humanMove(page, p.x + rand(-40, 40), p.y + rand(-20, 30), { steps: 6 });
    await sleep(350);
  }

  if (!planOk || !(await results.isVisible().catch(() => false))) {
    // Retry once via form submit shortcut
    console.log("retrying plan…");
    const retryWait = page.waitForResponse(
      (res) => res.url().includes("/api/plan") && res.request().method() === "POST",
      { timeout: 120000 },
    );
    await build.click({ force: true });
    try {
      const res = await retryWait;
      console.log("retry status", res.status());
    } catch (_) {
      /* continue */
    }
    await results.waitFor({ state: "visible", timeout: 60000 }).catch(() => null);
  }

  if (!(await results.isVisible().catch(() => false))) {
    await page.screenshot({ path: path.join(__dirname, "debug-no-results.png"), fullPage: true });
    throw new Error("Plan results never appeared — see debug-no-results.png");
  }

  await sleep(2200);
  await label(page, "three corridors back", 3000);
  await sleep(1600);

  // Scroll to results
  await results.scrollIntoViewIfNeeded();
  await sleep(1400);
  const map = page.locator(".map-shell");
  if (await map.count()) {
    const m = await boxCenter(map);
    await humanMove(page, m.x - 120, m.y - 80, { steps: 36 });
    await label(page, "corridor heatmap", 3000);
    await sleep(1000);
    // slow trace across map, then faster hop
    for (let i = 0; i <= 16; i++) {
      await humanMove(
        page,
        m.x - 180 + i * 24,
        m.y - 50 + Math.sin(i / 2) * 40,
        { steps: Math.floor(rand(10, 20)) },
      );
      await sleep(rand(140, 280));
    }
    await sleep(800);
    // quick hops to checkpoints
    for (let i = 0; i < 4; i++) {
      await humanMove(page, m.x - 80 + i * 55, m.y + rand(-30, 30), { steps: 8 });
      await sleep(rand(200, 400));
    }
    await circle(page, m.x + 40, m.y, 30);
    await label(page, "checkpoint colors = risk", 3400);
    await sleep(1500);
  }

  // Hover route cards
  const cards = page.locator(".route-card");
  const count = await cards.count();
  for (let i = 0; i < Math.min(count, 3); i++) {
    const card = cards.nth(i);
    await card.scrollIntoViewIfNeeded();
    const c = await boxCenter(card);
    await humanMove(page, c.x - 60, c.y - 40, { steps: Math.floor(rand(22, 40)) });
    await sleep(600);
    await humanMove(page, c.x, c.y, { steps: 14 });
    await sleep(rand(1100, 1600));
    if (i === 1) {
      await circle(page, c.x, c.y - 20, 24);
      await label(page, "recommended", 3200);
      await page.mouse.click(c.x, c.y);
      await sleep(1600);
    } else {
      await label(page, i === 0 ? "alternative" : "another option", 2400);
      await sleep(900);
    }
  }

  // Open checkpoint details on recommended
  const details = page.locator("details").nth(1);
  if (await details.count()) {
    const d = await boxCenter(details.locator("summary"));
    await humanMove(page, d.x, d.y, { steps: 26 });
    await label(page, "checkpoint ETAs", 2800);
    await page.mouse.click(d.x, d.y);
    await sleep(2200);
    await humanMove(page, d.x + 40, d.y + 80, { steps: 22 });
    await sleep(1800);
    await humanMove(page, d.x + 20, d.y + 140, { steps: 16 });
    await sleep(1400);
  }

  // Ranking explanation dwell on recommended card
  if (count > 1) {
    const rec = await boxCenter(cards.nth(1));
    await humanMove(page, rec.x - 40, rec.y - 30, { steps: 28 });
    await circle(page, rec.x, rec.y, 36);
    await label(page, "severe → high → avg risk → time", 4000);
    await sleep(2200);
  }

  // Slider again after plan (live refresh demo)
  await page.locator("#forecast").scrollIntoViewIfNeeded();
  await sleep(1000);
  p = await boxCenter(slider);
  await humanMove(page, p.box.x + 20, p.y, { steps: 32 });
  await label(page, "nudge forecast… refreshes live", 3400);
  await sleep(900);
  await page.mouse.move(p.box.x + 10, p.y);
  await page.mouse.down();
  for (let i = 1; i <= 20; i++) {
    await page.mouse.move(p.box.x + 10 + (p.box.width * 0.4 * i) / 20, p.y + rand(-1, 1), {
      steps: 3,
    });
    await sleep(rand(50, 120));
  }
  await page.mouse.up();
  await sleep(3500);
  await label(page, "waiting on live refresh…", 2500);
  await sleep(5000);

  // Compare cards once more after refresh
  await results.scrollIntoViewIfNeeded().catch(() => null);
  await sleep(1200);
  if (count > 0) {
    const c0 = await boxCenter(cards.nth(0));
    await humanMove(page, c0.x, c0.y, { steps: 24 });
    await sleep(1200);
    if (count > 1) {
      const c1 = await boxCenter(cards.nth(1));
      await humanMove(page, c1.x, c1.y, { steps: 20 });
      await sleep(1400);
    }
  }

  // Footer
  await page.evaluate(() => window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" }));
  await sleep(1600);
  await humanMove(page, 200, 820, { steps: 34 });
  await label(page, "Nominatim · OSRM · Open-Meteo", 3600);
  await sleep(1400);
  await humanMove(page, 720, 450, { steps: 40 });
  await sleep(2200);
  await label(page, "thanks for watching", 3800);
  await sleep(2800);

  const videoPath = await page.video().path();
  await context.close();
  await browser.close();

  // Remux/copy to final name via ffmpeg
  const { spawnSync } = await import("node:child_process");
  const res = spawnSync(
    "ffmpeg",
    ["-y", "-i", videoPath, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", FINAL],
    { encoding: "utf8" },
  );
  if (res.status !== 0) {
    console.error(res.stderr);
    throw new Error("ffmpeg remux failed");
  }
  console.log("WROTE", FINAL);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
