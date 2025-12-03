#!/usr/bin/env python3
"""
drive_diag_kali.py

Unified single-shot SMART diagnostic for HDD / SSD / NVMe.
Designed for Kali Linux field/forensics ISO usage.

Requirements:
 - Python 3.8+
 - smartctl (smartmontools)
 - lsblk (util-linux)

Usage:
  sudo ./drive_diag_kali.py
  sudo ./drive_diag_kali.py --device /dev/sda
  sudo ./drive_diag_kali.py --json out.json
"""

from __future__ import annotations
import argparse
import subprocess
import re
import json
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple

# ANSI color helpers
ANSI = {
    "RESET": "\033[0m",
    "BOLD": "\033[1m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
    "RED": "\033[31m",
    "CYAN": "\033[36m"
}

def ansi(text: str, color: str) -> str:
    return f"{ANSI.get(color, '')}{text}{ANSI['RESET']}"

def run_cmd(cmd: List[str], capture_output=True, text=True, check=False):
    try:
        r = subprocess.run(cmd, capture_output=capture_output, text=text, check=check)
        return r.returncode, r.stdout if r.stdout is not None else "", r.stderr if r.stderr is not None else ""
    except Exception as e:
        return 1, "", str(e)

def require_root():
    import os
    if os.geteuid() != 0:
        raise SystemExit("This script requires root. Run with sudo.")

def discover_disks() -> List[str]:
    """Discover block devices of type 'disk' via lsblk (returns device paths like /dev/sda, /dev/nvme0n1)."""
    rc, out, err = run_cmd(["lsblk", "-dn", "-o", "NAME,TYPE"])
    if rc != 0:
        raise RuntimeError(f"lsblk failed: {err.strip()}")
    devices = []
    for line in out.splitlines():
        parts = line.strip().split()
        if len(parts) >= 2 and parts[1] == "disk":
            devices.append("/dev/" + parts[0])
    return devices

def smartctl_all(dev: str) -> str:
    """Run smartctl -a with fallback to -x if available."""
    # first try -a
    rc, out, err = run_cmd(["smartctl", "-a", dev])
    if rc == 0 and out.strip():
        return out
    # fallback to -x
    rc, out, err = run_cmd(["smartctl", "-x", dev])
    if rc == 0 and out.strip():
        return out
    raise RuntimeError(f"smartctl failed for {dev}: {err.strip() or out.strip()}")

# ---- Parsing helpers ----

def find_first_regex(text: str, patterns: List[str], flags=0) -> Optional[str]:
    for p in patterns:
        m = re.search(p, text, flags)
        if m:
            return m.group(1).strip()
    return None

def parse_int_from(text: str, patterns: List[str]) -> Optional[int]:
    s = find_first_regex(text, patterns, re.IGNORECASE)
    if not s:
        return None
    # remove commas and non-digit
    s = re.sub(r"[^\d]", "", s)
    if not s:
        return None
    return int(s)

def parse_floats_from(text: str, patterns: List[str]) -> Optional[float]:
    s = find_first_regex(text, patterns, re.IGNORECASE)
    if not s:
        return None
    try:
        return float(re.sub(r"[, ]", "", s))
    except:
        return None

# Generic attribute table parser to find SMART attributes by name
def parse_attr_table(text: str) -> Dict[str, Dict[str,str]]:
    """
    Parses the attribute table portion commonly presented by smartctl.
    Returns dict keyed by attribute name (e.g., 'Reallocated_Sector_Ct') -> {raw columns}
    This is best-effort and will only parse rows that look like attribute lines.
    """
    attrs = {}
    # common attr line format: ID ATTRIBUTE_NAME FLAG VALUE WORSE THRESH TYPE UPDATED WHEN_FAILED RAW_VALUE
    for line in text.splitlines():
        # skip header lines
        if re.match(r"^\s*ID#\s+ATTRIBUTE_NAME", line):
            continue
        # match typical numeric attribute rows starting with ID
        m = re.match(r"^\s*(\d+)\s+([\w\-]+)\s+.*\s+(\d+)\s+(\d+)\s+(\d+)\s+[\w-]+\s+[\w-]+\s+(-|[A-Za-z0-9_]+)\s+(.+)$", line)
        if m:
            # id = m.group(1)
            name = m.group(2)
            raw = m.group(9).strip()
            attrs[name] = {
                "id": m.group(1),
                "value": m.group(3),
                "worst": m.group(4),
                "thresh": m.group(5),
                "raw": raw
            }
            continue
        # alternate format: NAME | VALUE | ... (NVMe or other)
        m2 = re.match(r"^\s*([\w\-\_]+)\s+[-:]\s+(.+)$", line)
        if m2:
            name = m2.group(1)
            raw = m2.group(2).strip()
            attrs.setdefault(name, {})["raw"] = raw
    return attrs

# Specific parsing functions
def get_power_on_hours(text: str, attrs: Dict[str, Dict[str,str]]) -> Optional[int]:
    # Common attribute names
    candidates = [
        r"Power_On_Hours.*?(-?\d+)",
        r"Power on hours:\s*([0-9]+)",
        r"Power_On_Hours.*?raw_value\s*=\s*([0-9]+)",
        r"Power_On_Hours.*?Raw_Value.*?([0-9]+)",
    ]
    # check table attrs first
    for name in ("Power_On_Hours", "Power_On_Hours_and_Msec", "Power_On_Hour", "PowerOnHours"):
        if name in attrs:
            raw = attrs[name].get("raw", "")
            # extract left-most integer
            m = re.search(r"(\d+)", raw)
            if m:
                return int(m.group(1))
    # fallback to regex search
    for p in candidates:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            try:
                return int(m.group(1))
            except:
                continue
    # try NVMe "Power On Hours" line
    m = re.search(r"Power On Hours:\s*([0-9]+)", text, re.IGNORECASE)
    if m:
        return int(m.group(1))
    return None

def get_manufacture_date(text: str) -> Optional[str]:
    # common forms: Date of manufacture: YYYY-MM-DD, Manufacturing date: YYYY-MM-DD, Manufactured: YYYY-MM-DD
    patterns = [
        r"Date of manufacture[:\s]+([0-9]{4}-[0-9]{2}-[0-9]{2})",
        r"Manufacturing date[:\s]+([0-9]{4}-[0-9]{2}-[0-9]{2})",
        r"Manufactured[:\s]+([0-9]{4}-[0-9]{2}-[0-9]{2})",
        r"Manufacture Date[:\s]+([0-9]{4}-[0-9]{2}-[0-9]{2})",
    ]
    d = find_first_regex(text, patterns, re.IGNORECASE)
    if d:
        return d
    # sometimes shown as "Manufactured: MM/DD/YYYY" or "Manufactured: YYYY.MM.DD"
    patterns2 = [
        r"Manufactured[:\s]+([0-9]{2}/[0-9]{2}/[0-9]{4})",
        r"Date of Manufacture[:\s]+([0-9]{2}/[0-9]{2}/[0-9]{4})",
        r"Manufactured[:\s]+([0-9]{4}\.[0-9]{2}\.[0-9]{2})",
    ]
    s = find_first_regex(text, patterns2, re.IGNORECASE)
    if s:
        # normalize
        if "/" in s:
            try:
                dt = datetime.strptime(s, "%m/%d/%Y")
                return dt.strftime("%Y-%m-%d")
            except:
                pass
        if "." in s:
            try:
                dt = datetime.strptime(s, "%Y.%m.%d")
                return dt.strftime("%Y-%m-%d")
            except:
                pass
    # as a last-ditch attempt, look for "Manufactured in YYYY" or "Mfg date: YYYY"
    m = re.search(r"Manufactured.*?(20[0-9]{2}|19[0-9]{2})", text, re.IGNORECASE)
    if m:
        year = m.group(1)
        # default to Jan 01 of that year (approximation)
        return f"{year}-01-01"
    return None

def parse_temperature(attrs: Dict[str, Dict[str,str]], text: str) -> Dict[str, Optional[int]]:
    """
    Returns dict with keys: 'current', 'max', 'min' (ints in C) when available.
    Attempts multiple common formats.
    """
    out = {"current": None, "max": None, "min": None}
    # look in attribute table for Temperature_Celsius or Temperature
    for key in ("Temperature_Celsius", "Temperature", "Airflow_Temperature_Cel", "Temperature_Internal"):
        if key in attrs:
            raw = attrs[key].get("raw", "")
            m = re.search(r"(-?\d+)", raw)
            if m:
                out["current"] = int(m.group(1))
                break
    # try NVMe/other lines
    if out["current"] is None:
        m = re.search(r"Current Drive Temperature:\s*([0-9]+)C", text, re.IGNORECASE)
        if m:
            out["current"] = int(m.group(1))
    # find max temperature occurrences
    mmax = re.search(r"Temperature.*?Max.*?([0-9]+)", text, re.IGNORECASE)
    if mmax:
        try:
            out["max"] = int(mmax.group(1))
        except:
            pass
    # some smartctl prints "Temperature:  30 C (Min/Max 10/68)"
    m = re.search(r"Temperature:\s*[^\d\-]*([0-9]+)\s*C.*\(Min/Max\s*([0-9]+)\/([0-9]+)\)", text, re.IGNORECASE)
    if m:
        out["current"] = out["current"] or int(m.group(1))
        out["min"] = int(m.group(2))
        out["max"] = int(m.group(3))
    # alternate line "Temperature: 30 (Min 10, Max 68)"
    m2 = re.search(r"Temperature.*?([0-9]+).*Min.*?([0-9]+).*Max.*?([0-9]+)", text, re.IGNORECASE)
    if m2:
        out["current"] = out["current"] or int(m2.group(1))
        out["min"] = int(m2.group(2))
        out["max"] = int(m2.group(3))
    # NVMe lines "Temperature: 35 Celsius"
    if out["current"] is None:
        m3 = re.search(r"Temperature:\s*([0-9]+)\s*C", text, re.IGNORECASE)
        if m3:
            out["current"] = int(m3.group(1))
    # values may be strings — ensure integers or None
    for k in out:
        if out[k] is not None:
            try:
                out[k] = int(out[k])
            except:
                out[k] = None
    return out

def parse_realloc_pending_offline(attrs: Dict[str, Dict[str,str]], text: str) -> Dict[str, Optional[int]]:
    out = {"reallocated": None, "pending": None, "offline_uncorrectable": None}
    # attribute names to try
    names = {
        "reallocated": ["Reallocated_Sector_Ct", "Reallocated_Sector_Count", "Reallocated_Event_Count"],
        "pending": ["Current_Pending_Sector", "Current_Pending_Sectors"],
        "offline_uncorrectable": ["Offline_Uncorrectable", "Offline_Uncorrectable_Sector"]
    }
    for k, cand in names.items():
        for name in cand:
            if name in attrs:
                raw = attrs[name].get("raw", "")
                m = re.search(r"(-?\d+)", raw)
                if m:
                    out[k] = int(m.group(1))
                    break
    # fallback to regex search in raw text
    if out["reallocated"] is None:
        m = re.search(r"Reallocated_Sector.*?(\d+)", text, re.IGNORECASE)
        if m:
            out["reallocated"] = int(m.group(1))
    if out["pending"] is None:
        m = re.search(r"Current_Pending_Sector.*?(\d+)", text, re.IGNORECASE)
        if m:
            out["pending"] = int(m.group(1))
    if out["offline_uncorrectable"] is None:
        m = re.search(r"Offline_Uncorrectable.*?(\d+)", text, re.IGNORECASE)
        if m:
            out["offline_uncorrectable"] = int(m.group(1))
    return out

def parse_power_cycles(attrs: Dict[str, Dict[str,str]], text: str) -> Dict[str, Optional[int]]:
    out = {"power_cycle_count": None, "unsafe_shutdowns": None}
    if "Power_Cycle_Count" in attrs:
        raw = attrs["Power_Cycle_Count"].get("raw", "")
        m = re.search(r"(\d+)", raw)
        if m:
            out["power_cycle_count"] = int(m.group(1))
    if "Power_Cycle_Count" not in attrs:
        m = re.search(r"Power Cycle Count:\s*(\d+)", text, re.IGNORECASE)
        if m:
            out["power_cycle_count"] = int(m.group(1))
    # unsafe/unsafe shutdowns
    for name in ("Unsafe_Shutdowns", "Unsafe_shutdowns", "UnsafeShutdownCount"):
        if name in attrs:
            raw = attrs[name].get("raw", "")
            m = re.search(r"(\d+)", raw)
            if m:
                out["unsafe_shutdowns"] = int(m.group(1))
                break
    m2 = re.search(r"Unsafe shutdowns:\s*(\d+)", text, re.IGNORECASE)
    if out["unsafe_shutdowns"] is None and m2:
        out["unsafe_shutdowns"] = int(m2.group(1))
    return out

def parse_nvme_percent_used(text: str, attrs: Dict[str, Dict[str,str]]):
    # NVMe commonly reports "Percentage Used" or "Percent_Lifetime" or "Percentage Used:" line
    m = re.search(r"Percentage Used:\s*([0-9]+)%", text, re.IGNORECASE)
    if m:
        return int(m.group(1))
    m2 = re.search(r"Percent Used:\s*([0-9]+)%", text, re.IGNORECASE)
    if m2:
        return int(m2.group(1))
    # sometimes attr name is 'PercentageUsed' in raw table
    for k in ("Percentage_Used", "PercentageUsed", "Wear_Leveling_Count", "Media_Wearout_Indicator"):
        if k in attrs:
            raw = attrs[k].get("raw","")
            mm = re.search(r"(\d+)", raw)
            if mm:
                val = int(mm.group(1))
                # interpretation varies; assume it's percent used when <=100
                if 0 <= val <= 100:
                    return val
    return None

def parse_tbw_candidates(text: str, attrs: Dict[str, Dict[str,str]]) -> Optional[float]:
    """
    Attempt to determine Bytes Written (TB) from available fields.
    Tries to find:
     - Total_LBAs_Written (multiply by 512 bytes)
     - Data Units Written (NVMe) possibly with multiplier [x 512 bytes] or [x 1000 * 512]
    Returns TB (terabytes) as float or None.
    """
    # 1) Total_LBAs_Written attribute raw value like '123456789'
    for name in ("Total_LBAs_Written", "Total_LBAs_Written_Attribute", "Total_LBAs_Written"):
        if name in attrs:
            raw = attrs[name].get("raw","")
            m = re.search(r"(\d+)", raw.replace(",",""))
            if m:
                lbas = int(m.group(1))
                tb = lbas * 512 / (1000**4)  # convert to TB (decimal TB)
                return tb
    # 2) Look for "Data Units Written:   12345 [x 512 bytes]" NVMe output
    m = re.search(r"Data Units Written\s*:\s*([\d,]+)\s*\[?([^\]]*)\]?", text, re.IGNORECASE)
    if m:
        units = int(m.group(1).replace(",",""))
        extra = m.group(2)
        # unit multiplier: sometimes it's "x 512 bytes" or "x 1000 * 512 bytes"
        multi = 512
        mm = re.search(r"x\s*([\d,]+)\s*bytes", extra)
        if mm:
            try:
                multi = int(mm.group(1).replace(",", ""))
            except:
                pass
        # multiply
        total_bytes = units * multi
        tb = total_bytes / (1000**4)
        return tb
    # 3) Look for "Total Host Writes:" or "Host Writes" lines like "12345 GB"
    m2 = re.search(r"(Total_?Host_?Writes|Host_Writes|Host Writes|Total Host Writes).{0,20}([0-9\.,]+)\s*(GB|TB|MB)", text, re.IGNORECASE)
    if m2:
        val = float(m2.group(2).replace(",",""))
        unit = m2.group(3).upper()
        if unit == "MB":
            return val / 1000.0
        if unit == "GB":
            return val / 1000.0 / 1000.0
        if unit == "TB":
            return val
    return None

def parse_smart_overall(text: str) -> Optional[str]:
    m = re.search(r"SMART overall-health self-assessment test result:\s*([A-Za-z]+)", text, re.IGNORECASE)
    if m:
        return m.group(1).upper()
    m2 = re.search(r"SMART overall-health:\s*([A-Za-z]+)", text, re.IGNORECASE)
    if m2:
        return m2.group(1).upper()
    # NVMe "SMART Health Status: OK" or "SMART/Health Status: PASSED"
    m3 = re.search(r"SMART Health Status:\s*([A-Za-z]+)", text, re.IGNORECASE)
    if m3:
        return m3.group(1).upper()
    return None

def parse_self_test(text: str) -> Dict[str, str]:
    out = {"last_short": "UNKNOWN", "last_long": "UNKNOWN", "last_error": "NONE"}
    m = re.search(r"SMART.*Self-test.*\n(?:.|\n)*?#\s*1\s+.*", text, re.IGNORECASE)
    # try to find lines "Short self-test routine completed without error" and "Long self-test routine completed without error"
    if re.search(r"Short self-test.*completed without error", text, re.IGNORECASE):
        out["last_short"] = "PASSED"
    else:
        m2 = re.search(r"Short self-test.*(Failed|Completed).*", text, re.IGNORECASE)
        if m2:
            out["last_short"] = m2.group(0).strip()
    if re.search(r"Long self-test.*completed without error", text, re.IGNORECASE):
        out["last_long"] = "PASSED"
    else:
        m3 = re.search(r"Long self-test.*(Failed|Completed).*", text, re.IGNORECASE)
        if m3:
            out["last_long"] = m3.group(0).strip()
    # failing or error messages
    m4 = re.search(r"(Self-test.*(fail|error).*)", text, re.IGNORECASE)
    if m4:
        out["last_error"] = m4.group(1)
    # NVMe test lines
    m5 = re.search(r"Self-test log structure revision number.*\n(.+?)(\n\n|\Z)", text, re.IGNORECASE|re.DOTALL)
    if m5:
        # best-effort, don't over-interpret
        out["last_short"] = out["last_short"]
    return out

# ---- Utilities ----

def hours_to_yy_dd_hh(total_hours: int) -> Tuple[int,int,int]:
    days, hours = divmod(total_hours, 24)
    years, days = divmod(days, 365)
    return years, days, hours

def active_percentage(runtime_hours: int, manufacture_date: Optional[str]) -> Tuple[Optional[float], Optional[int]]:
    if not manufacture_date:
        return None, None
    try:
        mfg = datetime.strptime(manufacture_date, "%Y-%m-%d")
    except Exception:
        # attempt to parse other formats
        try:
            mfg = datetime.strptime(manufacture_date, "%Y/%m/%d")
        except:
            return None, None
    now = datetime.now()
    total_life_hours = int((now - mfg).total_seconds() / 3600)
    if total_life_hours <= 0:
        return None, total_life_hours
    pct = (runtime_hours / total_life_hours) * 100.0
    return pct, total_life_hours

def grade_health(metrics: Dict[str, Any]) -> Tuple[str,str]:
    """
    Return (grade, reason) where grade is 'GREEN'/'YELLOW'/'RED'
    """
    # immediate fail conditions
    if metrics.get("smart_overall") and metrics["smart_overall"].upper() in ("FAIL", "FAILED"):
        return "RED", "SMART overall-health reported FAILED"
    # offline uncorrectable or pending severe
    if metrics.get("offline_uncorrectable", 0) and metrics.get("offline_uncorrectable", 0) > 0:
        return "RED", f"Offline uncorrectable: {metrics.get('offline_uncorrectable')}"
    if metrics.get("pending", 0) and metrics.get("pending", 0) > 5:
        return "RED", f"Pending sectors: {metrics.get('pending')}"
    if metrics.get("reallocated", 0) and metrics.get("reallocated", 0) > 50:
        return "RED", f"High reallocated sectors: {metrics.get('reallocated')}"
    # yellow conditions
    if (metrics.get("reallocated", 0) and 0 < metrics.get("reallocated") <= 50) or (metrics.get("pending",0) and 0 < metrics.get("pending") <= 5):
        return "YELLOW", f"Reallocated/pending sectors moderate ({metrics.get('reallocated')}/{metrics.get('pending')})"
    pct_used = metrics.get("percent_used")
    if pct_used is not None:
        if pct_used >= 90:
            return "RED", f"SSD wear {pct_used}%"
        if pct_used >= 70:
            return "YELLOW", f"SSD wear {pct_used}%"
    # temperature checks
    cur_temp = metrics.get("temp_current")
    max_temp = metrics.get("temp_max")
    if cur_temp and cur_temp >= 65:
        return "YELLOW", f"High current temperature {cur_temp}C"
    if max_temp and max_temp >= 75:
        return "YELLOW", f"Historic max temperature {max_temp}C"
    # otherwise green
    return "GREEN", "No critical indicators"

# ---- Main per-device analysis ----

def analyze_device(dev: str) -> Dict[str, Any]:
    info: Dict[str, Any] = {"device": dev}
    text = smartctl_all(dev)
    info["raw_smart"] = None  # omit large block in JSON by default; populate if --raw requested
    # basic model/serial
    model = find_first_regex(text, [r"Device Model:\s*(.+)", r"Model Family:\s*(.+)", r"Model Number:\s*(.+)"], re.IGNORECASE)
    serial = find_first_regex(text, [r"Serial Number:\s*(.+)"], re.IGNORECASE)
    firmware = find_first_regex(text, [r"Firmware Version:\s*(.+)", r"Firmware Revision:\s*(.+)"], re.IGNORECASE)
    info.update({"model": model, "serial": serial, "firmware": firmware})

    attrs = parse_attr_table(text)

    # fields
    hours = get_power_on_hours(text, attrs)
    info["power_on_hours"] = hours

    # manufacture date - can be None
    mfg = get_manufacture_date(text)
    info["manufacture_date"] = mfg

    # runtime conversion & active pct
    if hours is not None:
        y,d,h = hours_to_yy_dd_hh(hours)
        info["runtime_yy_dd_hh"] = {"years": y, "days": d, "hours": h}
        pct, total_hours = active_percentage(hours, mfg)
        info["active_percentage"] = round(pct,2) if pct is not None else None
        info["hours_since_manufacture"] = total_hours
    else:
        info["runtime_yy_dd_hh"] = None
        info["active_percentage"] = None
        info["hours_since_manufacture"] = None

    # reallocated/pending/offline
    rp = parse_realloc_pending_offline(attrs, text)
    info.update(rp)

    # temps
    temps = parse_temperature(attrs, text)
    info["temp_current"] = temps.get("current")
    info["temp_max"] = temps.get("max")
    info["temp_min"] = temps.get("min")

    # power cycles etc
    pcycles = parse_power_cycles(attrs, text)
    info.update(pcycles)

    # NVMe/SSD wear & TBW
    percent_used = parse_nvme_percent_used(text, attrs)
    info["percent_used"] = percent_used

    tb = parse_tbw_candidates(text, attrs)
    info["tb_written_TB"] = round(tb,3) if tb is not None else None

    info["smart_overall"] = parse_smart_overall(text)
    info["self_test"] = parse_self_test(text)

    # grade
    grade, reason = grade_health(info)
    info["health_grade"] = grade
    info["health_reason"] = reason

    # Provide a short human-friendly summary string
    info["summary"] = f"{model or 'Unknown'} {serial or ''} - {info['health_grade']} ({info['health_reason']})"

    # raw text in case of troubleshooting; keep out by default
    info["_raw_smart_text_preview"] = "\n".join(text.splitlines()[:40])  # small preview

    return info

def print_report(info: Dict[str, Any]) -> None:
    dev = info.get("device")
    # colorize grade
    grade = info.get("health_grade","GREEN")
    color = "GREEN" if grade == "GREEN" else ("YELLOW" if grade == "YELLOW" else "RED")
    print(ansi(f"\n=== Device: {dev} ===", "CYAN"))
    print(ansi(f"{info.get('summary')}", color))
    print(f"Model: {info.get('model') or 'N/A'}")
    print(f"Serial: {info.get('serial') or 'N/A'}   Firmware: {info.get('firmware') or 'N/A'}")
    # runtime
    hours = info.get("power_on_hours")
    if hours is not None:
        ydh = info.get("runtime_yy_dd_hh", {})
        print(f"Power-On Hours: {hours}h  →  {ydh.get('years','?')}y:{ydh.get('days','?')}d:{ydh.get('hours','?')}h")
    else:
        print("Power-On Hours: N/A")

    if info.get("manufacture_date"):
        print(f"Manufacture Date: {info.get('manufacture_date')}   Hours since mfg: {info.get('hours_since_manufacture')}")
        if info.get("active_percentage") is not None:
            print(f"Active Usage: {info.get('active_percentage'):.2f}%")
    else:
        print("Manufacture Date: N/A (use --mfg override if known)")

    print("\n--- Health Metrics ---")
    print(f"SMART overall-health: {info.get('smart_overall') or 'UNKNOWN'}")
    print(f"Health Grade: {ansi(info.get('health_grade'), color)}  ({info.get('health_reason')})")
    print(f"Reallocated sectors: {info.get('reallocated')}")
    print(f"Current pending sectors: {info.get('pending')}")
    print(f"Offline uncorrectable: {info.get('offline_uncorrectable')}")
    if info.get("percent_used") is not None:
        print(f"SSD / NVMe percent used: {info.get('percent_used')}%")
    if info.get("tb_written_TB") is not None:
        print(f"Total bytes written (approx): {info.get('tb_written_TB')} TB")
    print("\n--- Environmental ---")
    print(f"Temp current: {info.get('temp_current') or 'N/A'} C   Max: {info.get('temp_max') or 'N/A'} C   Min: {info.get('temp_min') or 'N/A'} C")
    print("\n--- Power/IO ---")
    print(f"Power cycle count: {info.get('power_cycle_count')}")
    print(f"Unsafe shutdowns: {info.get('unsafe_shutdowns')}")
    print("\n--- Self-tests ---")
    st = info.get("self_test", {})
    print(f"Last short test: {st.get('last_short')}")
    print(f"Last long test:  {st.get('last_long')}")
    print(f"Last self-test error notes: {st.get('last_error')}")
    print("\n")

# ---- CLI ----

def main():
    parser = argparse.ArgumentParser(description="Unified SMART drive diagnostic (Kali-ready)")
    parser.add_argument("--device", "-d", help="Single device to scan (e.g. /dev/sda). If omitted, scan all disks.")
    parser.add_argument("--mfg", help="Override manufacture date (YYYY-MM-DD) for percentage calc (applies to all devices when scanning all).")
    parser.add_argument("--json", help="Write JSON report to file")
    parser.add_argument("--raw", action="store_true", help="Include raw smartctl output in JSON (can be large)")
    args = parser.parse_args()

    require_root()

    devices = [args.device] if args.device else discover_disks()
    if not devices:
        raise SystemExit("No block devices found to scan.")

    reports = []
    for dev in devices:
        try:
            info = analyze_device(dev)
            # if user provided manual manufacture date override, set it
            if args.mfg:
                info["manufacture_date"] = args.mfg
                if info.get("power_on_hours") is not None:
                    pct, total_hours = active_percentage(info["power_on_hours"], args.mfg)
                    info["active_percentage"] = round(pct,2) if pct is not None else None
                    info["hours_since_manufacture"] = total_hours
            reports.append(info)
            print_report(info)
        except Exception as e:
            print(ansi(f"ERROR scanning {dev}: {e}", "RED"))

    if args.json:
        out = {"generated_at": datetime.now().isoformat(), "reports": reports}
        if not args.raw:
            # remove raw smart text preview key already small; but ensure not to include big text
            for r in out["reports"]:
                r.pop("raw_smart", None)
        else:
            # include full raw smart output by calling smartctl -a again (expensive) and placing into report.raw_smart
            for r in out["reports"]:
                try:
                    rc, full, err = run_cmd(["smartctl", "-a", r["device"]])
                    r["raw_smart"] = full
                except:
                    r["raw_smart"] = None
        with open(args.json, "w") as f:
            json.dump(out, f, indent=2)
        print(f"JSON report written to {args.json}")

if __name__ == "__main__":
    main()
