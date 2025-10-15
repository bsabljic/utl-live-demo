from utl.detector import UTLDetector

def test_detector_runs():
    d = UTLDetector()
    h, c = d.update({"linguistic": 0.5, "behavioral": 0.3, "temporal": 0.2, "resilience": 0.1})
    assert 0.0 <= h <= 1.0
    assert isinstance(c, bool)
