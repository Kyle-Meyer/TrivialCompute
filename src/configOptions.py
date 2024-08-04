import sys
configModule = sys.modules[__name__]
configModule.optionalMatchOriginalColors = True
configModule.optionalStaticBoard = True
configModule.optionalThreeDimensionalTiles = True
configModule.optionalThreeDimensionalTokens = True
configModule.optionalTileBlackOutline = True
configModule.optionalDebugMode = False
configModule.optionalFastDice = True
configModule.optionalPruneNeighbors = True
configModule.optionalSkeletalDemoMode = False
configModule.optionalSkeletalDemoRolls = [4,2,6,3,5,5,3,4]
configModule.online = True

