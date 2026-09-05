#!/usr/bin/env python3
"""
ComfyUI에 설치된 노드들을 조회하는 유틸리티
ZImage, Flux 등 필요한 노드들이 실제로 어떤 이름으로 설치되어있는지 확인
"""

import requests
import json
import sys
from pathlib import Path


def get_output_path() -> Path:
    """ComfyUI 노드 정보 저장 경로를 반환한다."""
    project_root = Path(__file__).resolve().parents[1]
    output_dir = project_root / "workflows"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / "comfyui_nodes_info.json"


def check_comfyui_nodes(url="http://127.0.0.1:8188"):
    """ComfyUI에 설치된 모든 노드 조회"""
    try:
        # 1. 온라인 상태 확인
        resp = requests.get(f"{url}/system_stats", timeout=(0.5, 1.0))
        if resp.status_code != 200:
            print("❌ ComfyUI is not online")
            return False
        print("✅ ComfyUI is online")
        
        # 2. 전체 object_info 조회
        print("\n📋 Fetching all node information...")
        resp = requests.get(f"{url}/object_info", timeout=(1.0, 2.0))
        if resp.status_code != 200:
            print("❌ Failed to fetch object_info")
            return False
        
        obj_info = resp.json()
        
        # 3. 필요한 노드들 찾기
        required_nodes = [
            "UnetLoaderGGUF",
            "CLIPLoaderGGUF", 
            "DualCLIPLoaderGGUF",
            "VAELoader",
            "CheckpointLoaderSimple",
            "KSampler",
            "FluxGuidance",
        ]
        
        print("\n🔍 Checking for required nodes:")
        print("-" * 60)
        
        found_nodes = {}
        missing_nodes = []
        
        for node_name in required_nodes:
            if node_name in obj_info:
                found_nodes[node_name] = True
                print(f"  ✅ {node_name}")
            else:
                missing_nodes.append(node_name)
                print(f"  ❌ {node_name}")
        
        # 4. Z-Image 관련 커스텀 노드 찾기
        print("\n🔎 Looking for Z-Image related nodes:")
        print("-" * 60)
        zimage_keywords = ["zimage", "z_image", "turbo", "image_turbo"]
        zimage_nodes = [name for name in obj_info.keys() 
                       if any(kw in name.lower() for kw in zimage_keywords)]
        
        if zimage_nodes:
            for node in zimage_nodes:
                print(f"  ✅ {node}")
        else:
            print("  (No Z-Image specific nodes found)")
        
        # 5. Flux 관련 커스텀 노드 찾기
        print("\n🔎 Looking for Flux related nodes:")
        print("-" * 60)
        flux_keywords = ["flux"]
        flux_nodes = [name for name in obj_info.keys() 
                     if any(kw in name.lower() for kw in flux_keywords)]
        
        if flux_nodes:
            for node in flux_nodes:
                print(f"  ✅ {node}")
        else:
            print("  (No Flux specific nodes found)")
        
        # 6. 로더 관련 노드 찾기
        print("\n🔎 Looking for Loader nodes:")
        print("-" * 60)
        loader_keywords = ["loader", "load"]
        loader_nodes = [name for name in obj_info.keys() 
                       if any(kw in name.lower() for kw in loader_keywords)]
        
        for node in sorted(loader_nodes):
            print(f"  ℹ️  {node}")
        
        # 7. 요약
        print("\n" + "=" * 60)
        print("📊 SUMMARY")
        print("=" * 60)
        print(f"Total nodes installed: {len(obj_info)}")
        print(f"Required nodes found: {len(found_nodes)}/{len(required_nodes)}")
        if missing_nodes:
            print(f"Missing nodes: {', '.join(missing_nodes)}")
        else:
            print("✅ All required nodes are installed!")
        
        # 8. 상세 정보 저장
        output_file = get_output_path()
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "total_nodes": len(obj_info),
                "found_required": found_nodes,
                "missing_required": missing_nodes,
                "zimage_nodes": zimage_nodes,
                "flux_nodes": flux_nodes,
                "all_nodes": list(obj_info.keys())
            }, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Detailed info saved to: {output_file}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to ComfyUI")
        print(f"   Make sure ComfyUI is running at {url}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8188"
    success = check_comfyui_nodes(url)
    sys.exit(0 if success else 1)
