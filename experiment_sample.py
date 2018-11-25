"""
Generators a sample experiment
"""

from generators.user import user, TrackedVisit
from generators.population_segment import PopulationSegment
from generators.hour_functions import *

# Make a difference between men and women.
# Women have higher purchase rate overall
# Men are more affected by the variation, but the effect is smaller on mobile devices
