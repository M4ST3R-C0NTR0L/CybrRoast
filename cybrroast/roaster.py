"""
Roast generator for site-roast.

Generates funny, Gordon Ramsay-style commentary based on audit scores.
"""

import random
from typing import List


class Roaster:
    """
    Generates humorous roast commentary based on audit scores.
    
    Think Gordon Ramsay meets web development.
    """

    # Roast templates by score range
    HIGH_SCORE_ROASTS = [  # 95-100
        "Okay, this is actually fire. Respect. 🔥",
        "Chef's kiss. Someone knows what they're doing. 👨‍🍳",
        "I'd hire whoever built this. Outstanding work.",
        "Finally! A website that doesn't make me want to cry.",
        "This is so good, I'm suspicious. What's the catch?",
        "Plot twist: this website is actually good!",
    ]

    GOOD_SCORE_ROASTS = [  # 80-94
        "Not bad, not bad. Your SEO person deserves a raise.",
        "Solid B+. You're in the top 20% of websites I've seen today.",
        "This is like a decent restaurant meal. Won't win awards, but won't make you sick.",
        "Pretty good! Just a few rough edges to polish.",
        "I see potential here. A few tweaks and this could be great.",
        "Acceptable. Which is high praise coming from me.",
    ]

    MID_SCORE_ROASTS = [  # 60-79
        "Mid. Just... mid. Your website is the plain oatmeal of the internet.",
        "It's giving 'we did the bare minimum' vibes.",
        "Not terrible, but also not memorable. Like elevator music.",
        "Your website is the human equivalent of lukewarm coffee.",
        "I've seen worse. But I've also seen a lot better.",
        "This is the 'participation trophy' of websites.",
        "Functional, but about as exciting as a tax form.",
    ]

    LOW_SCORE_ROASTS = [  # 40-59
        "Yikes. Did an intern build this during their lunch break?",
        "This website has commitment issues. And by commitment, I mean committing to quality.",
        "I've seen more effort put into a 'coming soon' page.",
        "Your website is like a salad at a steakhouse — technically there, but why?",
        "Bold strategy making everything mediocre. Let's see if it pays off.",
        "This needs work. Like, 'pull an all-nighter' level work.",
    ]

    BAD_SCORE_ROASTS = [  # 20-39
        "I've seen better websites on GeoCities in 1998.",
        "This website is so slow, I aged 5 years waiting for it to load.",
        "Did you build this in Notepad... during a power outage?",
        "Your SEO is hiding like my motivation on a Monday morning.",
        "This site has more issues than a celebrity tabloid.",
        "Calling this 'unfinished' would be generous.",
        "Your website just asked me if it could copy my homework.",
    ]

    DISASTER_ROASTS = [  # 0-19
        "This isn't a website. This is a cry for help. 💀",
        "I've seen error pages with more effort than this.",
        "Congratulations, you've achieved '404 personality'.",
        "This website is the digital equivalent of a dumpster fire.",
        "I'm not saying your website is bad, but... actually yes I am. It's bad.",
        "Burn it down and start over. Trust me on this one.",
        "Your website called and asked if it could borrow some self-respect.",
        "If websites could feel shame, this one would need therapy.",
    ]

    # Overall summary roasts by grade
    GRADE_ROASTS = {
        "A+": [
            "Absolutely flawless. Are you sure you didn't cheat?",
            "I'm genuinely impressed. Take my money already!",
        ],
        "A": [
            "Excellent work! Someone actually cares about quality.",
            "Top tier website. You should be proud (and I don't say that often).",
        ],
        "A-": [
            "So close to perfect! Just a tiny bit more polish needed.",
            "Great job! The A- student who could easily be an A+.",
        ],
        "B+": [
            "Very solid effort. Above average in a sea of mediocrity.",
            "Good work! You're in the honors program of web development.",
        ],
        "B": [
            "Respectable B-tier website. Not exceptional, but competent.",
            "Decent job. You're passing with style.",
        ],
        "B-": [
            "Average with ambition. I see what you're trying to do.",
            "You're on the right track, just keep improving.",
        ],
        "C+": [
            "Slightly above average. The participation trophy of grades.",
            "Meh-plus. It's trying, I'll give it that.",
        ],
        "C": [
            "Definition of 'fine, I guess'. The vanilla ice cream of websites.",
            "Perfectly average. Not good, not bad, just... there.",
        ],
        "C-": [
            "Below average. Like getting a C- in 'Introduction to Breathing'.",
            "Needs significant improvement. Back to the drawing board.",
        ],
        "D+": [
            "Barely passing. Your website is one missed assignment away from failing.",
            "This is what 'doing the minimum' looks like.",
        ],
        "D": [
            "Failing but trying. Points for effort, I suppose.",
            "This needs serious work. Like, hire-a-professional serious.",
        ],
        "D-": [
            "Almost failing. Your website is holding on by a thread.",
            "Critical condition. Call a developer ASAP.",
        ],
        "F": [
            "Complete failure. This website is an insult to the internet.",
            "F stands for 'Find a new web developer'. Immediately.",
        ],
    }

    def __init__(self, no_roast: bool = False):
        """
        Initialize the roaster.
        
        Args:
            no_roast: If True, returns serious comments instead of roasts.
        """
        self.no_roast = no_roast

    def get_roast(self, score: int, category: str = "") -> str:
        """
        Get a roast comment based on score.
        
        Args:
            score: The audit score (0-100).
            category: Optional category name for context.
            
        Returns:
            A roast comment string.
        """
        if self.no_roast:
            return self._get_serious_comment(score)

        if score >= 95:
            roasts = self.HIGH_SCORE_ROASTS
        elif score >= 80:
            roasts = self.GOOD_SCORE_ROASTS
        elif score >= 60:
            roasts = self.MID_SCORE_ROASTS
        elif score >= 40:
            roasts = self.LOW_SCORE_ROASTS
        elif score >= 20:
            roasts = self.BAD_SCORE_ROASTS
        else:
            roasts = self.DISASTER_ROASTS

        return random.choice(roasts)

    def _get_serious_comment(self, score: int) -> str:
        """Get a serious, professional comment instead of a roast."""
        if score >= 95:
            return "Excellent. This category meets or exceeds best practices."
        elif score >= 80:
            return "Good. Minor improvements could push this to excellent."
        elif score >= 60:
            return "Acceptable. Some issues present but functional."
        elif score >= 40:
            return "Below average. Several issues need attention."
        elif score >= 20:
            return "Poor. Significant problems affecting this category."
        else:
            return "Critical. Immediate attention required for this area."

    def get_overall_roast(self, grade: str, score: int) -> str:
        """
        Get a summary roast based on overall grade.
        
        Args:
            grade: The letter grade (A+ to F).
            score: The numerical score.
            
        Returns:
            A summary roast string.
        """
        if self.no_roast:
            return f"Overall Score: {score}/100 (Grade: {grade})"

        roasts = self.GRADE_ROASTS.get(grade, self.GRADE_ROASTS["F"])
        return random.choice(roasts)

    def get_category_context(self, category: str, score: int) -> str:
        """
        Get category-specific roast context.
        
        Args:
            category: The category name.
            score: The score for that category.
            
        Returns:
            Contextual roast string.
        """
        if self.no_roast:
            return ""

        contexts = {
            "title": {
                "low": "Your title is so bad, even the browser tab is embarrassed.",
                "mid": "Title exists but it's as exciting as 'Document1.doc'.",
            },
            "meta_description": {
                "low": "No meta description? Google will just make something up. Probably about hamsters.",
                "mid": "Your meta description is the literary equivalent of elevator music.",
            },
            "headings": {
                "low": "Heading structure is a disaster. It's like a book with random chapter numbers.",
                "mid": "Your headings exist, which is the bare minimum. Congratulations on doing the bare minimum.",
            },
            "images": {
                "low": "Images without alt text are just digital decorations for sighted people. Rude.",
                "mid": "Some images have alt text. The rest are just guessing games for screen readers.",
            },
            "mobile": {
                "low": "Not mobile-friendly? What year is this, 2007?",
                "mid": "Sort of works on mobile. Like how a shoe sort of works as a hammer.",
            },
            "ssl_security": {
                "low": "No HTTPS? Your users' data is basically postcards in the mail.",
                "mid": "You have HTTPS, but your security headers are taking a nap.",
            },
            "performance": {
                "low": "This site is so slow, I made coffee while waiting for it to load.",
                "mid": "Not the fastest, but hey, patience is a virtue, right?",
            },
            "links": {
                "low": "Link structure is a maze with no exit. Good luck, users!",
                "mid": "Links work, but they could be better organized.",
            },
            "open_graph": {
                "low": "No Open Graph? Your social shares will look like sad text messages.",
                "mid": "Basic social tags present. Could use more flair for sharing.",
            },
            "schema": {
                "low": "No structured data. Google is playing guessing games with your content.",
                "mid": "Some schema markup. Enough to get by, not enough to excel.",
            },
        }

        category_key = category.lower().replace(" ", "_").replace("/", "_")
        cat_contexts = contexts.get(category_key, {})

        if score < 40:
            return cat_contexts.get("low", "")
        elif score < 70:
            return cat_contexts.get("mid", "")
        return ""
