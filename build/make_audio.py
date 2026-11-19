"""Pre-render every phrase / example / dialogue turn to MP3 with edge-tts.

iPhone Safari blocks speechSynthesis in silent mode, so the app plays these files.
Voices: female ja-JP-NanamiNeural, male ja-JP-KeitaNeural.
"""
import asyncio, os, sys, json
import edge_tts
import contentlib

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "audio")
VOICE = {"f": "ja-JP-NanamiNeural", "m": "ja-JP-KeitaNeural"}
SEM = asyncio.Semaphore(6)
FORCE = "--force" in sys.argv


def jobs():
    data = contentlib.processed()
    out = []
    for p in data["phrases"]:
        out.append(("p_" + p["id"], p["jp"], VOICE[p["v"]]))
        out.append(("e_" + p["id"], p["ex"], VOICE[p["v"]]))
    for d in data["dialogues"]:
        for i, l in enumerate(d["lines"]):
            v = d["a"] if l["r"] == "A" else d["b"]
            out.append(("d%s_%d" % (d["id"], i), l["jp"], VOICE[v]))
    return out


async def one(name, text, voice):
    path = os.path.join(OUT, name + ".mp3")
    if not FORCE and os.path.exists(path) and os.path.getsize(path) > 800:
        return (name, "skip", 0)
    async with SEM:
        for attempt in range(4):
            try:
                c = edge_tts.Communicate(text, voice)
                await c.save(path)
                size = os.path.getsize(path)
                if size > 800:
                    return (name, "ok", size)
            except Exception as e:  # network hiccup / throttling
                if attempt == 3:
                    return (name, "fail:" + str(e)[:80], 0)
                await asyncio.sleep(1.5 * (attempt + 1))
        return (name, "fail:empty", 0)


async def main():
    os.makedirs(OUT, exist_ok=True)
    js = jobs()
    print("total jobs:", len(js), flush=True)
    done = 0
    fails = []
    for coro in asyncio.as_completed([one(*j) for j in js]):
        name, status, size = await coro
        done += 1
        if status.startswith("fail"):
            fails.append((name, status))
        if done % 40 == 0:
            print("  %d/%d" % (done, len(js)), flush=True)
    print("done. failures:", len(fails))
    for f in fails[:20]:
        print("  FAIL", f)


asyncio.run(main())
