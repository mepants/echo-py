#!/usr/bin/python3 -u

#Sample init message:
#{"id": 0, "src": "c0", "dest": "n1", "body": {"type": "init", "node_id": "n1", "node_ids": ["n1"], "msg_id": 1}}

import sys
import json
import copy

def reply(node_id, dest, msg_id, body, type):
    response_body = copy.deepcopy(body)
    response_body["msg_id"] = msg_id
    response_body["in_reply_to"] = body["msg_id"]
    response_body["type"] = type

    response = {
        "src": node_id,
        "dest": dest,
        "body": response_body
    }

    sys.stdout.write(json.dumps(response) + "\n")

def main():
    node_id = None
    msg_id = 0

    for line in sys.stdin:
        msg = json.loads(line)
        sys.stderr.write("Received: " + json.dumps(msg) + "\n")

        body = msg["body"]
        if body["type"] == "init":
            node_id = body["node_id"]
            sys.stderr.write("Node ID: " + str(node_id))

            msg_id += 1
            reply(node_id, msg["src"], msg_id, body, "init_ok")
        elif body["type"] == "echo":
            msg_id += 1
            reply(node_id, msg["src"], msg_id, body, "echo_ok")

if __name__ == "__main__":
    main()

