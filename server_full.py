"""Loan desk MCP server: the four agent tools in one file.

Install:  pip install "mcp[cli]<2"
Run:      mcp dev server.py
All data is fake and for demonstration only.
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("gambia-loan-demo")

KNOWN_IDS = {
    "NIN-1988-847291": "TIN-908123-GM",  # Fatou Ceesay
    "NIN-1994-102938": "TIN-445129-GM",  # Dawda Jallow
    "NIN-1981-992384": "TIN-112930-GM",  # Lamin Touray
}
WATCHLIST = {"example pep person"}  # fake PEP list for the demo


@mcp.tool()
def verify_nin_and_tin(nin: str, tin: str) -> dict:
    """Agent 1 (KYC): check a National ID and tax number."""
    ok = KNOWN_IDS.get(nin) == tin
    return {"status": "MATCH" if ok else "NO_MATCH"}


@mcp.tool()
def query_interbank_defaults(nin: str, debt: float, income: float) -> dict:
    """Agent 2 (Credit): debt-to-income ratio and a risk label."""
    if income <= 0:
        return {"nin": nin, "error": "income must be greater than zero"}
    ratio = debt / income
    if ratio < 0.25:
        risk = "LOW_RISK"
    elif ratio < 0.55:
        risk = "MEDIUM_RISK"
    else:
        risk = "HIGH_RISK"
    return {"nin": nin, "debt_to_income": round(ratio, 2), "risk": risk}


@mcp.tool()
def assess_land_deed(asset_id: str) -> dict:
    """Agent 3 (Collateral): is there valid collateral on file?"""
    valid = "unsecured" not in asset_id.lower()
    return {"deed_valid": valid}


@mcp.tool()
def screen_pep_and_sanctions(name: str) -> dict:
    """Agent 4 (AML): screen a name against the demo watchlist."""
    hit = name.strip().lower() in WATCHLIST
    return {"pep": hit, "status": "FLAGGED" if hit else "CLEARED"}


if __name__ == "__main__":
    mcp.run()  # stdio by default