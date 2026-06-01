#!/usr/bin/env python3
"""Generate the public Kill Log archive (index.html) from the real KILLLOG.md
receipts. stdlib-only. v1: static page, brand aesthetic. Run: python3 build.py"""
import html
import os

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "receipts.md")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")


def parse(path):
    rows = []
    for line in open(path):
        s = line.rstrip("\n")
        if s.startswith("|") and "---" not in s and "when (UTC)" not in s:
            cells = [c.strip() for c in s.strip().strip("|").split("|")]
            if len(cells) >= 7:
                rows.append(cells[:7])  # when, task, tried, verdict, why, metric, value
    return rows


def badge(v):
    v = v.lower()
    if v == "kept":
        return "KEPT", "#3FB950"
    if v == "killed":
        return "KILLED", "#FF5252"
    return v.upper(), "#d29922"  # rejected / other


def esc(s):
    return html.escape(s)


def main():
    rows = parse(SRC)
    kept = sum(1 for r in rows if r[3].lower() == "kept")
    cut = sum(1 for r in rows if r[3].lower() in ("killed", "rejected"))
    cards = []
    for when, task, tried, verdict, why, metric, value in reversed(rows):
        label, color = badge(verdict)
        cards.append(f"""
      <article class="rcpt">
        <div class="rcpt-h">
          <span class="badge" style="color:{color};border-color:{color}">{esc(label)}</span>
          <span class="task">{esc(task)}</span>
          <span class="when">{esc(when)} UTC</span>
        </div>
        <div class="tried">{esc(tried)}</div>
        <div class="why">{esc(why)}</div>
        <div class="metric"><span class="mk">{esc(metric)}</span> <span class="mv">{esc(value)}</span></div>
      </article>""")
    body = "\n".join(cards)
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kill Log — receipts</title>
<style>
  :root{{--bg:#0D1117;--line:#1C2430;--txt:#c9d1d9;--mut:#6e7681;--white:#e6edf3}}
  *{{box-sizing:border-box}} html,body{{margin:0;background:var(--bg);color:var(--txt)}}
  body{{font-family:'SF Mono','Menlo','Consolas','Liberation Mono',monospace;line-height:1.5}}
  .wrap{{max-width:880px;margin:0 auto;padding:56px 22px 80px}}
  header h1{{font-size:46px;letter-spacing:2px;margin:0;color:var(--white)}}
  header h1 .strike{{position:relative}}
  header h1 .strike:after{{content:"";position:absolute;left:-4px;right:-4px;top:54%;height:6px;background:#FF5252;border-radius:3px}}
  .sub{{color:var(--mut);margin:14px 0 6px;font-size:16px}}
  .tally{{color:var(--mut);font-size:15px;margin-bottom:30px}}
  .tally b{{color:var(--white)}}
  .rcpt{{border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin:14px 0;background:#0e141c}}
  .rcpt-h{{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:10px}}
  .badge{{font-size:13px;font-weight:700;border:1px solid;border-radius:5px;padding:2px 9px;letter-spacing:1px}}
  .task{{color:var(--white);font-weight:700;font-size:17px}}
  .when{{color:var(--mut);font-size:13px;margin-left:auto}}
  .tried{{color:var(--txt);font-size:15px;margin:6px 0}}
  .why{{color:var(--mut);font-size:14px;margin:6px 0}}
  .metric{{margin-top:10px;font-size:14px}}
  .mk{{color:var(--mut)}} .mv{{color:var(--white);font-weight:700;border:1px solid var(--line);border-radius:5px;padding:1px 8px}}
  footer{{color:var(--mut);font-size:13px;margin-top:40px;border-top:1px solid var(--line);padding-top:18px}}
</style></head><body><div class="wrap">
  <header>
    <h1><span class="strike">KILL</span> LOG</h1>
    <p class="sub">An AI-agent company, built in public. A permanent record of every
    decision we kept and killed — with the real number. Receipts &gt; hype.</p>
    <p class="tally"><b>{kept}</b> kept &middot; <b>{cut}</b> killed &middot; append-only, no edits</p>
  </header>
  {body}
  <footer>Auto-generated from our live KILLLOG.md. The agents propose; the human keeps score.</footer>
</div></body></html>"""
    with open(OUT, "w") as f:
        f.write(page)
    print(f"wrote {OUT} — {len(rows)} receipts ({kept} kept, {cut} killed)")


if __name__ == "__main__":
    main()
