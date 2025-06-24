#this was re-written by chatGPT. But it works real good :)

# A lightweight utility that packs the contents of the ``dev`` folder into two
# PRAY‑format *.agents files for Docking Station.
#
# Part 1 (C2toDS_Refresh_Part1.agents)
#   • Includes the world‑map script (0.0_world_map.cos)
#   • Uses **its own** RSCR block as the remove script
#   • Uses ``moe_C2toDS_Thumbnail.c16`` as the agent thumbnail
#   • Bundles binary dependencies needed (just the thumbnail)
#
# Part 2 (C2toDS_Refresh_Part2.agents)
#   • Packs **all other** *.cos files (normal sections only)
#   • Holds a combined remove script made from every remaining RSCR block
#
# Both files are written to ``<current folder>/dev/My Agents``.
#
# Apart from the thumbnail, this only packs .cos files into the agents, to reduce file size.
# The other folders will be packed into the release separately :)


import os
import re
import struct
import zlib
from pathlib import Path
from typing import List, Tuple

############################################################
# Low‑level helpers                                         #
############################################################

def pray_write_binary_block(f, block_type: bytes, block_name: str, data: bytes) -> None:
    """Write a compressed PRAY FILE/BLK block."""
    assert len(block_type) == 4, "block_type must be four bytes"
    f.write(block_type)
    f.write(block_name.encode("cp1252"))
    f.write(b"\0" * (128 - len(block_name)))
    comp = zlib.compress(data)
    f.write(struct.pack("<III", len(comp), len(data), 1))
    f.write(comp)


def pray_write_tag_block(
    f, block_type: bytes, block_name: str, tags: dict[str, str | int]
):
    """Write a PRAY DSAG/C2DS tag block."""
    int_tags: dict[bytes, int] = {}
    str_tags: dict[bytes, bytes] = {}
    for k, v in tags.items():
        if isinstance(v, int):
            int_tags[k.encode("cp1252")] = v
        else:
            str_tags[k.encode("cp1252")] = str(v).encode("cp1252")

    buf = bytearray()
    buf += struct.pack("<I", len(int_tags))
    for k, v in int_tags.items():
        buf += struct.pack("<I", len(k)) + k + struct.pack("<I", v)
    buf += struct.pack("<I", len(str_tags))
    for k, v in str_tags.items():
        buf += struct.pack("<I", len(k)) + k + struct.pack("<I", len(v)) + v

    pray_write_binary_block(f, block_type, block_name, bytes(buf))

############################################################
# Helpers                                                  #
############################################################

def split_cos(text: str) -> Tuple[str, List[str]]:
    """Return (normal_section, list_of_rscr_sections)."""
    parts = re.split(r"(?m)^\s*rscr[\s$]", text)
    return parts[0], parts[1:]

def read_cos(path: Path) -> str:
    """Read a .cos file using CP‑1252 encoding."""
    return path.read_text(encoding="cp1252")

############################################################
# Collection                                               #
############################################################

CURRENT = Path(__file__).resolve().parent
DEV     = CURRENT / "dev"
SCRIPTS = DEV / "Scripts"
THUMB   = DEV / "images" / "moe_C2toDS_Thumbnail.c16"

# Ensure output directory exists
OUTPUT_DIR = CURRENT / DEV / "My Agents"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

scripts: List[Path] = sorted(SCRIPTS.rglob("*.cos"))
world_map = SCRIPTS / "0.0_world_map.cos"
if world_map not in scripts:
    raise FileNotFoundError("0.0_world_map.cos not found in Scripts")

other_scripts = [p for p in scripts if p != world_map]

dependencies: List[Path] = []
if THUMB.exists():
    dependencies.append(THUMB)

############################################################
# Build Part 1                                             #
############################################################

PART1_PATH  = OUTPUT_DIR / "C2toDS_Refresh_Part1.agents"
PART1_TITLE = "C2toDS Refresh"
PART1_DESC  = "C2 to DS Refresh!!!"

print(f"Writing {PART1_PATH.name} …")
with PART1_PATH.open("wb") as f:
    f.write(b"PRAY")

    tags: dict[str, str | int] = {
        "Agent Type": 0,
        "Agent Description": PART1_DESC,
        "Agent Animation File": THUMB.name,  # thumbnail file (with extension)
        "Agent Sprite First Image": "1",
        "Agent Animation Gallery": THUMB.stem,  # thumbnail gallery name (no .c16)
        "Dependency Count": len(dependencies),
        "Web URL": "https://github.com/Creatures-Developer-Network/C2toDS-Refresh/",
        "Web Label": "C2toDS-Refresh on GitHub",
    }

    # --‑ Dependencies first so they appear immediately after the count --‑
    for idx, dep in enumerate(dependencies, 1):
        ext = dep.suffix.lower().lstrip(".")
        if ext in ("mng", "wav"):
            cat = 1
        elif ext in ("c16", "s16"):
            cat = 2
        elif ext == "blk":
            cat = 6
        elif ext == "catalogue":
            cat = 7
        else:
            raise RuntimeError(f"Unknown dependency category for {dep}")

        tags[f"Dependency {idx}"] = dep.name
        tags[f"Dependency Category {idx}"] = cat

        pray_write_binary_block(f, b"FILE", dep.name, dep.read_bytes())

    # --‑ World‑map script & its RSCR --‑
    normal, rscrs = split_cos(read_cos(world_map))
    tags["Script Count"] = 1
    tags["Script 1"] = f"* {world_map.name}\r\n" + normal.strip() + "\r\n"

    tags["Remove script"] = (
        "\r\n".join(
            f"* {world_map.name}\r\n" + r.strip() for r in rscrs
        ) + "\r\n"
        if rscrs
        else ""
    )

    pray_write_tag_block(f, b"DSAG", PART1_TITLE, tags)
print("Part 1 done")

############################################################
# Build Part 2                                             #
############################################################

PART2_PATH  = OUTPUT_DIR / "C2toDS_Refresh_Part2.agents"
PART2_TITLE = "C2toDS Refresh HIDDEN AGENTS"
PART2_DESC  = (
    "Bulk of the cos files for C2toDS, injected after the map is loaded."
)

print(f"Writing {PART2_PATH.name} …")
with PART2_PATH.open("wb") as f:
    f.write(b"PRAY")

    tags: dict[str, str | int] = {
        "Agent Type": 0,
        "Agent Description": PART2_DESC,
        "Agent Animation File": "blnk.c16",
        "Agent Sprite First Image": "1",
        "Agent Animation Gallery": "blnk",
        "Dependency Count": 0,
        "Script Count": len(other_scripts),
        "Web URL": "https://github.com/Creatures-Developer-Network/C2toDS-Refresh/",
        "Web Label": "C2toDS-Refresh on GitHub",
    }

    combined_rscr: List[str] = []
    for idx, path in enumerate(other_scripts, 1):
        normal, rscrs = split_cos(read_cos(path))
        rel_name = os.path.relpath(path, CURRENT)
        tags[f"Script {idx}"] = f"* {rel_name}\r\n" + normal.strip() + "\r\n"
        for r in rscrs:
            combined_rscr.append(f"* {rel_name}\r\n" + r.strip() + "\r\n")

    tags["Remove script"] = "\r\n".join(combined_rscr)

    pray_write_tag_block(f, b"C2DS", PART2_TITLE, tags)
print("Part 2 done")

input("All done! Press Enter to exit…")
