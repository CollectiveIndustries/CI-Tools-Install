import json

def loadJsonDebugData_():
    """Pulls a JSON file returns the data.
    Used primarily for debugging"""
    with open(_lsblkDataFile_) as json_data:
        return json.load(json_data)