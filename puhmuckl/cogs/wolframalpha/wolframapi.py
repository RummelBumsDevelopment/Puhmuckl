import requests
import logging

import urllib.parse
from util import config
import xml.etree.ElementTree as ET

class WolframImage:
    def __init__(self, node: ET.Element):
        self.src    = node.attrib["src"]
        self.alt    = node.attrib["alt"]
        self.title  = node.attrib["title"]
        self.width  = node.attrib["width"]
        self.height = node.attrib["height"]

class WolframSubPod:
    def __init__(self, node: ET.Element):
        self.image = None
        self.plaintext = None

        self.parse(node)

    def parse(self, node: ET.Element):
        image = node.find("img")
        if image is not None:
            self.image = WolframImage(image)

        plaintext = node.find("plaintext")
        if plaintext is not None:
            self.plaintext = plaintext.text


class WolframPod:
    def __init__(self, node: ET.Element):
        self.subpods = []
        self.parse(node)

    def parse(self, node: ET.Element):
        self.title      = node.attrib["title"]
        self.error      = node.attrib["error"]
        self.position   = node.attrib["position"]
        self.scanner    = node.attrib["scanner"]
        self.id         = node.attrib["id"]
        self.numsubpods = node.attrib["numsubpods"]

        for tag in node.findall("subpod"):
            self.subpods.append(WolframSubPod(tag))


class WolframDidYouMean:
    def __init__(self, node: ET.Element):
        self.score = float(node.attrib["score"])
        self.content = node.text


class WolframResponse:
    API_ENDPOINT = "http://api.wolframalpha.com/v2/query?appid={0}&input={1}"

    def __init__(self, query: str):
        self.query = query
        self.pods = []
        self.did_you_means = []

        self.send()
        root_node = ET.fromstring(self.response_text)
        self.parse(root_node)


    def send(self):
        response = requests.get(
            WolframResponse.API_ENDPOINT.format(
                config.get_config('AUTHORIZATION','wolframalpha'), 
                urllib.parse.quote(self.query)
            )
        )

        logging.debug(response.text)

        self.response_text = response.text

    def parse(self, root_node: ET.Element):
        self.success        = (root_node.attrib["success"] == "true")
        self.error          = root_node.attrib["error"]
        self.numpods        = int(root_node.attrib["numpods"])
        self.version        = root_node.attrib["version"]
        self.datatypes      = root_node.attrib["datatypes"].split(",")
        self.timing         = float(root_node.attrib["timing"])
        self.timedout       = root_node.attrib["timedout"]
        self.parsetiming    = float(root_node.attrib["parsetiming"])
        self.parsetimedout  = root_node.attrib["parsetimedout"]
        self.recalculate    = root_node.attrib["recalculate"]

        did_you_mean = root_node.find("didyoumean")
        if did_you_mean is not None:
            for tag in did_you_mean.findall("didyoumean"):
                self.did_you_means.append(WolframDidYouMean(tag))
            
            self.did_you_means.sort(key = lambda x : x.score)
            return

        for node in root_node.findall("pod"):
            self.pods.append(WolframPod(node))

        self.pods.sort(key = lambda x : x.position)
