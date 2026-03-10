"""
Scoring logic for site-roast.

Provides utilities for calculating and normalizing scores.
"""

from typing import List, Optional


class ScoreCalculator:
    """
    Utility class for calculating and manipulating scores.
    
    Provides methods for score normalization, grading, and statistical
    operations on audit scores.
    """

    @staticmethod
    def normalize_score(value: float, min_val: float, max_val: float, 
                       target_min: int = 0, target_max: int = 100) -> int:
        """
        Normalize a value to a score between target_min and target_max.
        
        Args:
            value: The value to normalize.
            min_val: Minimum expected value.
            max_val: Maximum expected value.
            target_min: Minimum target score.
            target_max: Maximum target score.
            
        Returns:
            Normalized score as integer.
        """
        if max_val == min_val:
            return target_max
        
        normalized = (value - min_val) / (max_val - min_val)
        normalized = max(0, min(1, normalized))  # Clamp to 0-1
        
        score = int(normalized * (target_max - target_min) + target_min)
        return max(target_min, min(target_max, score))

    @staticmethod
    def calculate_average(scores: List[int]) -> int:
        """
        Calculate the average of multiple scores.
        
        Args:
            scores: List of scores.
            
        Returns:
            Average score rounded to nearest integer.
        """
        if not scores:
            return 0
        return round(sum(scores) / len(scores))

    @staticmethod
    def score_to_grade(score: int) -> str:
        """
        Convert a numerical score to a letter grade.
        
        Args:
            score: Score from 0-100.
            
        Returns:
            Letter grade (A+ to F).
        """
        if score >= 97:
            return "A+"
        elif score >= 93:
            return "A"
        elif score >= 90:
            return "A-"
        elif score >= 87:
            return "B+"
        elif score >= 83:
            return "B"
        elif score >= 80:
            return "B-"
        elif score >= 77:
            return "C+"
        elif score >= 73:
            return "C"
        elif score >= 70:
            return "C-"
        elif score >= 67:
            return "D+"
        elif score >= 63:
            return "D"
        elif score >= 60:
            return "D-"
        else:
            return "F"

    @staticmethod
    def grade_description(grade: str) -> str:
        """
        Get a description for a letter grade.
        
        Args:
            grade: Letter grade.
            
        Returns:
            Description string.
        """
        descriptions = {
            "A+": "Exceptional - exceeds all expectations",
            "A": "Excellent - meets best practices",
            "A-": "Very Good - minor improvements needed",
            "B+": "Good - above average",
            "B": "Above Average - competent work",
            "B-": "Average Plus - acceptable with room for improvement",
            "C+": "Slightly Above Average - meets minimum standards",
            "C": "Average - acceptable but unremarkable",
            "C-": "Below Average - needs work",
            "D+": "Poor - significant issues present",
            "D": "Very Poor - major improvements needed",
            "D-": "Critical - barely functional",
            "F": "Failing - requires complete overhaul",
        }
        return descriptions.get(grade, "Unknown")

    @staticmethod
    def penalty(score: int, penalty_amount: int, min_score: int = 0) -> int:
        """
        Apply a penalty to a score.
        
        Args:
            score: Original score.
            penalty_amount: Amount to subtract.
            min_score: Minimum allowed score.
            
        Returns:
            Score after penalty.
        """
        return max(min_score, score - penalty_amount)

    @staticmethod
    def bonus(score: int, bonus_amount: int, max_score: int = 100) -> int:
        """
        Apply a bonus to a score.
        
        Args:
            score: Original score.
            bonus_amount: Amount to add.
            max_score: Maximum allowed score.
            
        Returns:
            Score after bonus.
        """
        return min(max_score, score + bonus_amount)

    @staticmethod
    def weighted_average(scores: List[int], weights: List[int]) -> int:
        """
        Calculate a weighted average of scores.
        
        Args:
            scores: List of scores.
            weights: List of weights (must sum to 100 or be normalized).
            
        Returns:
            Weighted average score.
        """
        if len(scores) != len(weights):
            raise ValueError("Scores and weights must have same length")
        
        if not scores:
            return 0
        
        # Normalize weights if they don't sum to 100
        total_weight = sum(weights)
        if total_weight != 100:
            weights = [w / total_weight * 100 for w in weights]
        
        weighted_sum = sum(s * (w / 100) for s, w in zip(scores, weights))
        return round(weighted_sum)


class ScoreThresholds:
    """
    Standard thresholds for categorizing scores.
    """
    
    EXCELLENT = 90
    GOOD = 75
    AVERAGE = 60
    POOR = 40
    CRITICAL = 20
    
    @classmethod
    def categorize(cls, score: int) -> str:
        """
        Categorize a score into a qualitative bucket.
        
        Args:
            score: The score to categorize.
            
        Returns:
            Category string.
        """
        if score >= cls.EXCELLENT:
            return "excellent"
        elif score >= cls.GOOD:
            return "good"
        elif score >= cls.AVERAGE:
            return "average"
        elif score >= cls.POOR:
            return "poor"
        elif score >= cls.CRITICAL:
            return "critical"
        else:
            return "disaster"
    
    @classmethod
    def get_threshold(cls, category: str) -> int:
        """
        Get the threshold value for a category.
        
        Args:
            category: Category name.
            
        Returns:
            Threshold value.
        """
        thresholds = {
            "excellent": cls.EXCELLENT,
            "good": cls.GOOD,
            "average": cls.AVERAGE,
            "poor": cls.POOR,
            "critical": cls.CRITICAL,
        }
        return thresholds.get(category.lower(), 0)
