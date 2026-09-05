#!/usr/bin/env python3
"""
특정 노드의 상세 정보 확인 유틸리티
"""

import requests
import json
import sys

def check_node_details(node_name, url="http://127.0.0.1:8188"):
    """특정 노드의 상세 정보 조회"""
    try:
        resp = requests.get(f"{url}/object_info/{node_name}", timeout=(0.5, 1.0))
        if resp.status_code != 200:
            print(f"❌ Node not found: {node_name}")
            return False
        
        data = resp.json()
        print(f"\n{'='*60}")
        print(f"📋 Node: {node_name}")
        print(f"{'='*60}")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_node_details.py <node_name> [<node_name2> ...]")
        print("\nExample:")
        print("  python check_node_details.py TextEncodeZImageOmni")
        print("  python check_node_details.py TextEncodeZImageOmni CLIPTextEncode")
        sys.exit(1)
    
    for node_name in sys.argv[1:]:
        check_node_details(node_name)
