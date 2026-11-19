"""Extract three identified tables from Halifax's September 2025 board report."""
import re
import subprocess
from source_io import fetch, publish

SOURCE = "https://www.halifax.ca/media/91695"
AGENCIES = ["Combined", "HRP", "RCMP"]
DISTRICTS = {"HRP":["Central Division","East Division","West Division"],
             "RCMP":["Lower Sackville","Cole Harbour","Tantallon","Musquodoboit Harbour","Sheet Harbour","North Central"]}
MEASURES = {"Public-generated calls":"Public-Generated Calls",
            "Officer proactive calls":"Proactive Calls","Online reports":"Online Reports"}


def numbers(line):
    return [int(n.replace(",", "")) for n in re.findall(r"-?\d[\d,]*",line)]


def extract(text):
    lines = text.split("Figure 1 – HRP and RCMP HRD Calls for Service", 1)[1].splitlines()
    calls = {agency:{} for agency in AGENCIES}
    for name, label in MEASURES.items():
        idx = next(i for i,line in enumerate(lines) if line.strip().startswith(label))
        data = [s for s in lines[idx:] if s.strip()][:3]
        for agency, line in zip(AGENCIES,data):
            if agency != "Combined" and not line.strip().startswith(agency):
                raise ValueError("Agency order changed")
            current, previous, change, _percent = numbers(line)
            if current - previous != change:
                raise ValueError(f"Invalid change for {name}")
            calls[agency][name] = [previous,current]
    district_rows = {}
    for agency, places in DISTRICTS.items():
        district_rows[agency] = {}
        for place in places:
            label = "Musquodoboit" if place == "Musquodoboit Harbour" else place
            match = re.search(r"^\s*" + label + r"\s+(\d[\d,]*\s+\d[\d,]*\s+\d[\d,]*\s+\d[\d,]*\s+\d+%)",text,re.M)
            if not match:
                raise ValueError(f"Missing district {place}")
            row = numbers(match[1])[:4]
            if sum(row[:3]) != row[3]:
                raise ValueError(f"Check district row {place}")
            district_rows[agency][place] = row
    return {"calls":calls,"districts":district_rows,"start":"2024-01","end":"2025-06","source":SOURCE}


if __name__ == "__main__":
    result = subprocess.run(["pdftotext","-layout","-","-"], input=fetch(SOURCE), capture_output=True, check=True)
    publish(extract(result.stdout.decode()))
