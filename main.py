# import the necessary modules and libraries
import json
import unittest
import datetime

# Load the JSON files
with open("./data-1.json", "r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json", "r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json", "r") as f:
    jsonExpectedResult = json.load(f)

def convertFromFormat1(jsonObject):
    """
    Converts telemetry data from Format 1 to the unified format.
    Location is parsed from a single string separated by slashes.
    """
    location_parts = jsonObject["location"].split("/")
    
    result = {
        'deviceID': jsonObject['deviceID'],
        'deviceType': jsonObject['deviceType'],
        'timestamp': jsonObject['timestamp'],
        'location': {
            'country': location_parts[0],
            'city': location_parts[1],
            'area': location_parts[2],
            'factory': location_parts[3],
            'section': location_parts[4]
        },
        'data': {
            'status': jsonObject['operationStatus'],
            'temperature': jsonObject['temp']
        }
    }
    return result

def convertFromFormat2(jsonObject):
    """
    Converts telemetry data from Format 2 to the unified format.
    ISO 8601 timestamp is converted to milliseconds since epoch.
    """
    # Replace 'Z' with UTC offset to ensure compatibility with fromisoformat
    iso_string = jsonObject['timestamp'].replace('Z', '+00:00')
    dt_obj = datetime.datetime.fromisoformat(iso_string)
    
    # Calculate milliseconds since epoch
    # Relation: T_ms = seconds * 1000
    timestamp_ms = int(dt_obj.timestamp() * 1000)

    result = {
        'deviceID': jsonObject['device']['id'],
        'deviceType': jsonObject['device']['type'],
        'timestamp': timestamp_ms,
        'location': {
            'country': jsonObject['country'],
            'city': jsonObject['city'],
            'area': jsonObject['area'],
            'factory': jsonObject['factory'],
            'section': jsonObject['section']
        },
        'data': jsonObject['data']
    }
    return result

def main(jsonObject):
    # Determine which format is being passed based on the key structure
    if "device" in jsonObject:
        return convertFromFormat2(jsonObject)
    else:
        return convertFromFormat1(jsonObject)

# Test cases using unittest module
class TestSolution(unittest.TestCase):

    def test_sanity(self):
        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType1(self):
        result = main(jsonData1)
        self.assertEqual(result, jsonExpectedResult, 'Converting from Type 1 failed')

    def test_dataType2(self):
        result = main(jsonData2)
        self.assertEqual(result, jsonExpectedResult, 'Converting from Type 2 failed')

if __name__ == '__main__':
    unittest.main()
