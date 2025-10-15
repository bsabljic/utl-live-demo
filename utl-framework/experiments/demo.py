"""
Minimal working example of UTL framework.
"""
from utl.detector import UTLDetector
import numpy as np

def simulate_crisis_escalation():
    detector = UTLDetector()
    print("=== UTL Framework Demo ===\n")
    print("Simulating conversation with gradual escalation...\n")

    for t in range(1, 16):
        features = {
            "linguistic": min(0.9, 0.1 + t * 0.05),
            "behavioral": float(np.clip(0.3 + 0.1 * np.random.randn(), 0, 1)),
            "temporal": 0.2 if t > 10 else 0.1,
            "resilience": max(0, 0.5 - t * 0.03)
        }
        hazard, crisis = detector.update(features)
        recovery_window = detector.get_recovery_window()
        status = "🚨 CRISIS" if crisis else "✓ OK"
        print(f"Turn {t:2d}: Hazard={hazard:.3f} | Status={status} | Recovery Window={recovery_window:.1f} turns")

        # Announce first crisis detection
        if crisis and t == detector.history[-1][0] and sum(1 for _, _, c in detector.history if c) == 1:
            print(f"\n🔴 CRISIS DETECTED at turn {t}!")
            print(f"📊 Cumulative risk: {detector.theta_t:.2f}")
            print(f"⏰ Recovery window: {recovery_window:.1f} turns")
            print(f"💡 Recommend: Immediate counselor escalation\n")

if __name__ == "__main__":
    simulate_crisis_escalation()
