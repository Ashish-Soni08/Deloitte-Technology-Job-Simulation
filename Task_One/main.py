from datetime import datetime

import json

import logging

import unittest

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

####### DATA #######
with open("./data-1.json", "r") as f:
    jsonData1 = json.load(f)

with open("./data-2.json", "r") as f:
    jsonData2 = json.load(f)
####### DATA #######

####### EXPECTED OUTPUT #######
with open("./data-result.json", "r") as f:
    jsonExpectedResult = json.load(f)
####### EXPECTED OUTPUT #######

####### FUNCTIONS #######


# data-1.json
def convertFromFormat1(jsonObject):
    """
    Converts a JSON object from format 1 to a standardized format.

    This function extracts device information from a JSON object with a flat structure
    and transforms it into a nested dictionary. It specifically handles the location string,
    splitting it into its components, and logs the conversion process with the input and output.

    Args:
        jsonObject (dict): A dictionary containing device data in format 1.
            Expected keys include: "deviceID", "deviceType", "timestamp", "location" (a string with '/' delimiter),
            "operationStatus", and "temp".

    Returns:
        dict or None: A dictionary representing the transformed device data, with nested
        "location" and "data" dictionaries, or None if an error occurs during the conversion.
    """
    logging.info(f"Starting conversion from format 1 with input: {jsonObject}")

    try:
        # Splits the location string into its components, based on the '/' delimiter
        country, city, area, factory, section = jsonObject.get(
            "location").split("/")
        data = {
            "deviceID": jsonObject.get("deviceID"),
            "deviceType": jsonObject.get("deviceType"),
            "timestamp": jsonObject.get("timestamp"),
            "location": {
                "country": country,
                "city": city,
                "area": area,
                "factory": factory,
                "section": section
            },
            "data": {
                "status": jsonObject.get("operationStatus"),
                "temperature": jsonObject.get("temp")
            }
        }
        logging.info(
            f"Successfully converted data from format 1, output: {data}")
        return data
    except Exception as e:
        logging.error(f"Error converting data from format 1: {e}")
        return None


# data-2.json
def convertFromFormat2(jsonObject):
    """
    Converts a JSON object from format 2 to a standardized format.

    This function extracts device information from a JSON object with a nested structure
    and transforms it into a standardized dictionary. It specifically handles the timestamp,
    converting it to milliseconds, and logs the conversion process with the input and output.

    Args:
        jsonObject (dict): A dictionary containing device data in format 2.
            Expected keys include: "device" (with nested "id" and "type"), "timestamp" (ISO format string),
            "country", "city", "area", "factory", "section", and "data".

    Returns:
        dict or None: A dictionary representing the transformed device data, or None if an error occurs
        during conversion.
    """
    logging.info(f"Starting conversion from format 2 with input: {jsonObject}")
    try:
        original_timestamp = jsonObject.get("timestamp")
        # replace z to +00:00 for fromisoformat
        modified_timestamp = datetime.fromisoformat(
            original_timestamp.replace("Z", "+00:00"))
        # multiply by 1000 to convert to milliseconds
        modified_timestamp = int(modified_timestamp.timestamp() * 1000)

        data = {
            "deviceID": jsonObject.get("device").get("id"),
            "deviceType": jsonObject.get("device").get("type"),
            "timestamp": modified_timestamp,
            "location": {
                "country": jsonObject.get("country"),
                "city": jsonObject.get("city"),
                "area": jsonObject.get("area"),
                "factory": jsonObject.get("factory"),
                "section": jsonObject.get("section")
            },
            "data": jsonObject.get("data")
        }

        logging.info(
            f"Successfully converted data from format 2, output: {data}")
        return data

    except Exception as e:
        logging.error(f"Error converting data from format 2: {e}")
        return None


####### FUNCTIONS #######


####### TESTS #######
def main(jsonObject):

    result = {}

    if (jsonObject.get('device') == None):
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result


class TestSolution(unittest.TestCase):

    def test_sanity(self):

        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType1(self):

        result = main(jsonData1)
        self.assertEqual(result, jsonExpectedResult,
                         'Converting from Type 1 failed')

    def test_dataType2(self):

        result = main(jsonData2)
        self.assertEqual(result, jsonExpectedResult,
                         'Converting from Type 2 failed')


####### TESTS #######

if __name__ == '__main__':
    unittest.main()
