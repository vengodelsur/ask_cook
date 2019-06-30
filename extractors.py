from natasha.extractors import Extractor
from natasha.crf import CrfTagger
from natasha.data import get_path

# кароч я не доразобрался как кастомные классы писать

FOOD_MODEL = get_path('models', 'food.crf.json')
TOOL_MODEL = get_path('models', 'tool.crf.json')
CHEF_ACTION_MODEL = get_path('models', 'chef_action.crf.json')
FOOD_ACTION_MODEL = get_path('models', 'food_action.crf.json')
TOOL_STATE_MODEL = get_path('models', 'tool_state.crf.json')
FOOD_STATE_MODEL = get_path('models', 'food_state.crf.json')


class FoodExtractor(Extractor):
    """
    Extracts ingredients, intermediate products, and the
    final dish in cooking.
    """
    def __init___(self):
		tagger = CrfTagger(
			FOOD_MODEL,
			get_food_features
		)
		super(FoodExtractor, self).__init__(
			FOOD,
			tagger=tagger
		)


class ToolExtractor(Extractor):
    """
    Extracts Extractors such as cookwares, jars, bottles, and knives
    are tools.
    """
    def __init__(self):
		tagger = CrfTagger(
			TOOL_MODEL,
			get_tool_features
		)
		super(FoodExtractor, self).__init__(
			TOOL,
			tagger=tagger
		)


class DurationExtractor(Extractor):
    """
    Extracts expressions to denote duration of a cooking action, such as
    heating time. This includes numbers and units.
    """
    def __init__(self):
		pass


class ChefActionExtractor(Extractor):
    """
    Extracts expressions to specify the quantity of foods. They are mainly 
    number expressions followed by units.
    """
    def __init__(self):
		tagger = CrfTagger(
			CHEF_ACTION_MODEL,
			get_chef_action_features
		)
		super(FoodExtractor, self).__init__(
			CHEF_ACTION,
			tagger=tagger
		)


class FoodActionExtractor(Extractor):
    """
    Extracts actions taken by the chef.
    """
    def __init__(self):
		tagger = CrfTagger(
			FOOD_ACTION_MODEL,
			get_food_action_features
		)
		super(FoodExtractor, self).__init__(
			FOOD_ACTION,
			tagger=tagger
		)


class ToolStateExtractor(Extractor):
    """
    Extracts actions taken by food.
    """
    def __init__(self):
		tagger = CrfTagger(
			TOOL_STATE_MODEL,
			get_tool_state_features
		)
		super(FoodExtractor, self).__init__(
			TOOL_STATE,
			tagger=tagger
		)


class FoodStateExtractor(Extractor):
    """
    Extracts expression describing taste, color, etc
    """
    def __init__(self):
		tagger = CrfTagger(
			FOOD_STATE_MODEL,
			get_food_state_features
		)
		super(FoodExtractor, self).__init__(
			FOOD_STATE,
			tagger=tagger
		)


class UnitExtractor(Extractor):
	"""
	Extracts expression like kilograms, meters, inches, etc
	"""
