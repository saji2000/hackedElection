import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_votes = []
        
    def new_block(self):
        pass

    def new_vote(self):
        pass

    @staticmethod
    def hash(block):
        pass

    @property
    def last_block(self):
        pass

print("hello")
