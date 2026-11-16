#!/usr/bin/env python3
"""
3D Web Prompt Generator

Generates optimized AI prompts for 3D web development based on task type
and target AI harness (OpenCode, Claude Code, ChatGPT).

Usage:
    python generate_3d_prompt.py --task "hero-scene" --harness "opencode"
"""

import argparse
import json
from typing import Dict, List

PROMPT_TEMPLATES = {
    "opencode": {
        "hero-scene": {
            "title": "Hero 3D Interactive Canvas Scene",
            "template": """You are a Senior 3D Web Developer specializing in Three.js and React Three Fiber (R3F).
Please generate a production-ready R3F Hero Scene component called `HeroExperience.jsx`.

Requirements:
1. **Canvas & Camera**:
   - Set up PerspectiveCamera at position [0, 1.5, 5] with FOV 50.
   - Configure WebGLRenderer with antialias, DPR capped at [1, 2], and outputColorSpace = SRGBColorSpace.
2. **Lighting**:
   - Add ambientLight (intensity: 0.4).
   - Add directionalLight (position: [5, 10, 5], intensity: 1.5, castShadow: true).
   - Set shadow map type to PCFSoftShadowMap.
3. **Interactive 3D Geometry**:
   - Create a floating geometric object (e.g., RoundedBox) with a MeshPhysicalMaterial.
   - Add subtle floating animation on the Y-axis using Math.sin inside useFrame.
   - Add hover state with smooth scaling (1.2x).
4. **Performance & Memory Protection**:
   - Pre-allocate Vector3 objects for lerping.
   - Implement clean resource disposal on unmount."""
        },
        "scroll-experience": {
            "title": "GSAP Scroll-Driven 3D Storytelling",
            "template": """Create a multi-step scroll-driven 3D experience using React Three Fiber and GSAP ScrollTrigger.
Architecture:
- Wrap canvas with <ScrollControls pages={4}> from @react-three/drei.
- Use useScroll() hook to read scroll progress.
- In useFrame, lerp camera position/rotation to keyframe targets.
Keyframes:
  - Page 0: Camera [0, 2, 6], lookAt [0, 0, 0]
  - Page 1: Camera [4, 1, 3], lookAt [0, 0, 0]
  - Page 2: Camera [-3, -1, 4], lookAt [0, 0, 0]
  - Page 3: Camera [0, 0, 5]
Add HTML overlays that fade based on scroll thresholds."""
        },
        "performance-audit": {
            "title": "3D Performance Audit Request",
            "template": """Review this 3D WebGL/R3F code for performance bottlenecks and memory leaks.
Checklist:
1. Are there setState calls inside useFrame? Convert to ref mutations.
2. Are new objects allocated inside loops? Pre-allocate them.
3. Are geometries/materials disposed on unmount?
4. Is InstancedMesh used for >50 repeated objects?
5. Are textures compressed with SRGBColorSpace?

Return refactored code with inline comments explaining each fix.
Input code: {code}"""
        }
    },
    "claude": {
        "shader": {
            "title": "Custom GLSL Shader",
            "template": """You are an expert GLSL shader developer. Generate a THREE.ShaderMaterial for WebGL2.

Specifications:
1. Vertex Shader: 
   - Displace vertices using 3D Simplex noise
   - Animate with uTime uniform (passed from clock.getElapsedTime())
   - Expose uAmplitude and uFrequency uniforms

2. Fragment Shader:
   - Sample input texture (uTexture sampler2D)
   - Calculate distortion offset from vertex displacement
   - Apply chromatic aberration (RGB channel offset)

3. React Integration:
   - Provide R3F component wrapper
   - Use extend({ShaderMaterial}) pattern

Math formulas for noise: {noise_formula}"""
        },
        "state-manager": {
            "title": "3D Zustand State Manager",
            "template": """Design a Zustand store for R3F 3D scene state management.

Requirements:
1. Camera state (position, target, fov)
2. Selection state (selected mesh id)
3. Animation state (isAnimating boolean, progress value)
4. UI overlay visibility

Write the TypeScript code with proper typing for THREE.Vector3, THREE.Euler, etc.
Include a quick example of how components consume this store.

Follow this naming convention: use3dStore = create(state => ({...}))"""
        }
    },
    "chatgpt": {
        "visual-effect": {
            "title": "Visual Shader Effect Concept",
            "template": """Generate raw GLSL code for this visual effect: {effect_description}

Style: {style}
Inspiration: {inspiration}

I need:
1. Vertex shader code with noise-based deformation
2. Fragment shader code with color manipulation
3. React Three Fiber integration snippet
4. Performance estimate (FPS budget)

Be expressive but technically precise. No placeholders - working code only."""
        },
        "product-viewer": {
            "title": "Product 3D Configurator",
            "template": """Build a React 3D product configurator that lets users rotate, zoom, and change colors of a product model.

Features:
1. OrbitControls with damping enabled
2. Multiple material variants (color swatches)
3. Product info overlay (HTML on top of 3D canvas)
4. "Add to Cart" button with 3D animation feedback

Write production-ready React + R3F code. Assume an exported GLB model at /model.glb.

Include loading state with <Html> from Drei."""
        }
    },
    "cursor": {
        "tweak": {
            "title": "Material & Light Tweaks",
            "template": """Optimize the material and lighting settings for the current 3D scene.

Current settings (inline in code):
{material_settings}

Provide inline-editable tweaks:
1. Recommended metalness/roughness values for {material_type}
2. Directional light position for soft shadows on product models
3. Ambient occlusion intensity
4. HDR environment map suggestion

Format: comment-only changes ready for copy-paste."""
        }
    }
}

def generate_prompt(task: str, harness: str, **kwargs) -> str:
    """Generate a prompt based on task and harness."""
    if harness not in PROMPT_TEMPLATES:
        raise ValueError(f"Unknown harness: {harness}. Available: {list(PROMPT_TEMPLATES.keys())}")
    
    if task not in PROMPT_TEMPLATES[harness]:
        raise ValueError(f"Unknown task: {task}. Available for {harness}: {list(PROMPT_TEMPLATES[harness].keys())}")
    
    template = PROMPT_TEMPLATES[harness][task]
    prompt = template['template']
    
    # Fill in any kwargs
    for key, value in kwargs.items():
        prompt = prompt.replace(f"{{{key}}}", str(value))
    
    return f"### {template['title']}\n\n{prompt}"

def main():
    parser = argparse.ArgumentParser(description="Generate AI prompts for 3D web development")
    parser.add_argument('--task', required=True, help='Task name (e.g., hero-scene, shader)')
    parser.add_argument('--harness', required=True, help='AI harness (opencode, claude, chatgpt, cursor)')
    parser.add_argument('--code', help='Code to analyze/audits')
    parser.add_argument('--effect', help='Visual effect description for ChatGPT')
    parser.add_argument('--style', help='Visual style')
    parser.add_argument('--inspiration', help='Inspiration source')
    parser.add_argument('--noise-formula', help='Math formula for noise')
    parser.add_argument('--material-settings', help='Current material settings')
    parser.add_argument('--material-type', help='Type of material (glass, metal, fabric)')
    
    args = parser.parse_args()
    
    kwargs = {
        'code': args.code,
        'effect_description': args.effect,
        'style': args.style,
        'inspiration': args.inspiration,
        'noise_formula': args.noise_formula,
        'material_settings': args.material_settings,
        'material_type': args.material_type
    }
    
    try:
        prompt = generate_prompt(args.task, args.harness, **kwargs)
        print(prompt)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()