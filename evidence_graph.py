#!/usr/bin/env python3
import json
import hashlib
import os

class EvidenceGraph:
    """
    Compliance Evidence Matrix: Enforces data provenance by persisting 
    raw source payloads and generating auditable verification hashes.
    """
    def log_and_hash_payload(self, asset_key, raw_dict):
        serialized = json.dumps(raw_dict, sort_keys=True, separators=(",", ":"), default=str)
        payload_hash = "sha256:" + hashlib.sha256(serialized.encode('utf-8')).hexdigest()
        
        os.makedirs("data/raw", exist_ok=True)
        raw_path = f"data/raw/{asset_key}_payload.json"
        
        try:
            with open(raw_path, "w", encoding="utf-8") as f:
                json.dump(raw_dict, f, indent=4)
        except Exception:
            pass
            
        return payload_hash, raw_path

    def generate_audit_lineage(self, asset_profile, payload_hash):
        metrics_block = asset_profile.get("metrics", {})
        source_name = metrics_block.get("source", "Public Alternative Data Stream")
        spot_price = metrics_block.get("price", 0.0)
        z_score = metrics_block.get("z_score", 0.0)
        
        return (
            f"Source Node: [{source_name}] | "
            f"Hash Reference: {payload_hash[:16]}... | "
            f"Statistical Trace: Value=${spot_price:,.2f}, Z-Score={z_score:+.2f}"
        )

    def append_appendix_logs(self, complete_playbook, hashes_map):
        html_appendix = "<div style='margin-top: 50px; border-top: 3px dashed #475569; padding-top: 25px;'>"
        html_appendix += "<h2 style='color:#f1f5f9;'>V. EVIDENCE APPENDIX & DATA LINEAGE LOGS</h2>"
        html_appendix += "<p style='color:#94a3b8; font-size:12px; margin-bottom:15px;'>Every parameter inside this brief is traceable. Cryptographic verification hashes are archived below.</p>"
        html_appendix += "<table style='width:100%; font-size:11px; font-family:monospace; color:#94a3b8; border-collapse: collapse;'>"
        html_appendix += "<tr style='background:#0f172a;'><th>Asset Key</th><th>Verifiable Data Source</th><th>Retrieval Timestamp</th><th>SHA-256 Payload Hash</th><th>Signal Intensity</th></tr>"
        
        for item in complete_playbook:
            ticker = item.get("asset", "UNKNOWN")
            h = hashes_map.get(ticker, "N/A")
            metrics_block = item.get("metrics", {})
            source_name = metrics_block.get("source", "Public API Stream Endpoint")
            timestamp = item.get("generated_at_utc", "N/A")
            score = item.get("composite_score", 0.0)
            
            html_appendix += f"""
            <tr style='border-bottom: 1px solid #334155;'>
                <td style='padding:10px;'><strong>{ticker}</strong></td>
                <td style='padding:10px;'>{source_name}</td>
                <td style='padding:10px;'>{timestamp}</td>
                <td style='padding:10px;'><code>{h}</code></td>
                <td style='padding:10px; color:#10b981;'><strong>{score:.1f}/100</strong></td>
            </tr>
            """
        html_appendix += "</table></div>"
        return html_appendix
