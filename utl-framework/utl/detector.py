"""
UTL Framework: Core Detector Class
Implements Algorithm 1 (minimal viable demo)
"""
import numpy as np
from typing import Dict, Tuple, List

class UTLDetector:
    """
    Temporal risk detection using EWMA hazard accumulation.

    Parameters:
        alpha (float): EWMA decay parameter (default: 0.15)
        theta_mult (float): Threshold multiplier (default: 1.5)
        gamma (float): Coupling coefficient (default: 1.5)
        beta (float): Resilience weight (default: 0.8)
        tau (float): Crisis threshold (default: 0.68)
    """

    def __init__(
        self,
        alpha: float = 0.15,
        theta_mult: float = 1.5,
        gamma: float = 1.5,
        beta: float = 0.8,
        tau: float = 0.68
    ):
        self.alpha = alpha
        self.theta_mult = theta_mult
        self.gamma = gamma
        self.beta = beta
        self.tau = tau

        # State variables
        self.v_t = 0.0  # EWMA variance-like accumulator
        self.theta_t = 0.0  # cumulative risk
        self.turn = 0
        self.history: List[Tuple[int, float, bool]] = []

    def update(self, features: Dict[str, float]) -> Tuple[float, bool]:
        """
        Process one conversation turn.

        Args:
            features: Dict with keys 'linguistic', 'behavioral',
                      'temporal', 'resilience'

        Returns:
            (hazard, crisis_flag): Current hazard and whether crisis detected
        """
        self.turn += 1

        # Aggregate risk signal (toy aggregation)
        r_t = (features.get('linguistic', 0.0) +
               features.get('behavioral', 0.0) +
               features.get('temporal', 0.0)) / 3.0

        # EWMA accumulation
        self.v_t = self.alpha * (r_t ** 2) + (1 - self.alpha) * self.v_t

        # Adaptive threshold from history variance (fallback to 1.0)
        if self.history:
            hist_vals = [h for _, h, _ in self.history]
            theta_adapt = self.theta_mult * (np.var(hist_vals) + 1e-6)
        else:
            theta_adapt = 1.0

        s = 0.5 * theta_adapt if theta_adapt > 0 else 0.5
        # Logistic hazard
        h_t = 1.0 / (1.0 + np.exp(-(self.v_t - theta_adapt) / max(s, 1e-6)))

        # Coupled hazard (simplified) with resilience
        h_net = h_t - self.beta * features.get('resilience', 0.0)
        h_net = float(np.clip(h_net, 0.0, 1.0))

        # Cumulative risk
        self.theta_t += h_net

        # Crisis flag
        crisis = h_net > self.tau

        # Store history
        self.history.append((self.turn, h_net, crisis))

        return h_net, crisis

    def get_recovery_window(self, theta_irrev: float = 10.0, epsilon: float = 0.1) -> float:
        """
        Estimate recovery window W(t) in turns (rough heuristic).
        """
        if len(self.history) < 5:
            return float("inf")

        recent_hazards = [h for _, h, _ in self.history[-5:]]
        lambda_t = (recent_hazards[-1] - recent_hazards[0]) / 5.0

        if lambda_t <= 0:
            return float("inf")

        W = (1.0 / lambda_t) * np.log(max((theta_irrev - self.theta_t), 1e-6) / max(epsilon, 1e-6))
        return float(max(0.0, W))

    def reset(self):
        """Reset detector state for a new conversation."""
        self.v_t = 0.0
        self.theta_t = 0.0
        self.turn = 0
        self.history = []
