from typing import Any, Dict, List


class ProcessingResult:
    def __init__(self):
        self.normalized: List[Dict[str, Any]] = []
        self.quarantined: List[Dict[str, Any]] = []
        self.stats: Dict[str, Any] = {
            "total_in": 0,
            "total_out": 0,
            "total_quarantined": 0,
            "errors_by_type": {}
        }
    
    def add_normalized(self, event: Dict[str, Any]):
        self.normalized.append(event)
        self.stats["total_out"] += 1
    
    def add_quarantined(self, raw_event: Dict[str, Any], errors: List[str]):
        self.quarantined.append({
            "raw": raw_event,
            "errors": errors
        })
        self.stats["total_quarantined"] += 1
        for error in errors:
            self.stats["errors_by_type"][error] = self.stats["errors_by_type"].get(error, 0) + 1
    
    def set_total_in(self, count: int):
        self.stats["total_in"] = count
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "normalized": self.normalized,
            "quarantined": self.quarantined,
            "stats": self.stats
        }
