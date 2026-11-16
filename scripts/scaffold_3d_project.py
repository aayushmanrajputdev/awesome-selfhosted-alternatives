#!/usr/bin/env python3
"""
3D Web Project Scaffolder

Scaffolds a complete 3D web project structure with best-practice configurations,
optimized for AI-assisted development workflows.

Usage:
    python scaffold_3d_project.py --type "react-r3f" --name "my-3d-app"
"""

import argparse
import json
from pathlib import Path
from dataclasses import dataclass
from typing import List

@dataclass
class ProjectFiles:
    name: str
    files: dict

def generate_vite_config(project_name: str) -> str:
    return f"""import {{ defineConfig }} from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({{
  plugins: [react()],
  server: {{
    port: 3000,
    open: true
  }},
  build: {{
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {{
      output: {{
        manualChunks: {{
          'three-js': ['three', '@react-three/fiber', '@react-three/drei'],
          'ui': ['framer-motion', '@react-spring/three']
        }}
      }}
    }}
  }}
}})
"""

def generate_package_json(project_name: str, use_r3f: bool = True) -> str:
    deps = {
        "react": "^18.2.0",
        "react-dom": "^18.2.0",
        "@vitejs/plugin-react": "^4.2.0",
        "vite": "^5.2.0",
    }
    
    if use_r3f:
        deps.update({
            "@react-three/fiber": "^8.15.11",
            "@react-three/drei": "^9.106.0",
            "three": "^0.162.0",
            "@react-spring/three": "^9.8.2",
            "gsap": "^3.12.5"
        })
    
    extras = {
        "eslint": "^8.57.0",
        "eslint-config-prettier": "^9.1.0",
        "prettier": "^3.2.5",
        "@types/react": "^18.2.66",
        "@types/react-dom": "^18.2.22",
        "typescript": "^5.4.5"
    }
    
    pkg = {"name": project_name, "version": "0.1.0", "private": True, "dependencies": deps, "devDependencies": extras}
    return json.dumps(pkg, indent=2)

def generate_tsconfig() -> str:
    return """{
  "compilerOptions": {
    "target": "ES2022",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "lib": ["DOM", "DOM.Iterable", "ES2022"],
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true
  },
  "include": ["src"]
}
"""

def generate_eslint_config() -> str:
    return """module.exports = {
  root: true,
  extends: ['eslint:recommended', 'prettier'],
  plugins: [],
  env: { browser: true, es2022: true },
  parserOptions: { ecmaVersion: 2022, sourceType: 'module' },
  rules: {
    'no-unused-vars': ['error', { argsIgnorePattern: '^_' }]
  }
}
"""

def generate_postcss_config() -> str:
    return """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""

def generate_tailwind_config() -> str:
    return """module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: { extend: {} },
  plugins: [],
}
"""

def generate_vite_html(title: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"""

def generate_main_jsx() -> str:
    return """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
"""

def generate_landing_tsx() -> str:
    return """import { Canvas } from '@react-three/fiber'
import { Suspense } from 'react'
import { Html, OrbitControls, Environment, ContactShadows } from '@react-three/drei'

function Box() {
  return (
    <mesh rotation={[0.4, 0.2, 0]}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="orange" />
    </mesh>
  )
}

function Scene() {
  return (
    <>
      <color attach="background" args={['#f0f0f0']} />
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 5, 5]} intensity={1} />
      <Box />
      <ContactShadows
        position={[0, -0.8, 0]}
        opacity={0.5}
        scale={2}
        blur={1}
      />
      <Environment preset="sunset" />
    </>
  )
}

export default function App() {
  return (
    <div style={{ height: '100vh' }}>
      <Canvas camera={{ position: [0, 0, 5], fov: 50 }}>
        <Suspense fallback={<Html center>Loading...</Html>}>
          <Scene />
        </Suspense>
      </Canvas>
    </div>
  )
}
"""

def scaffold_project(project_type: str, project_name: str, output_dir: str):
    """Generate complete project structure."""
    base = Path(output_dir) / project_name
    
    files = {
        'package.json': generate_package_json(project_name, project_type == 'r3f'),
        'vite.config.js': generate_vite_config(project_name),
        'tsconfig.json': generate_tsconfig(),
        '.eslintrc.cjs': generate_eslint_config(),
        'postcss.config.js': generate_postcss_config(),
        'tailwind.config.js': generate_tailwind_config(),
        'index.html': generate_vite_html(f"{project_name} - AI 3D Project"),
        'src/main.jsx': generate_main_jsx(),
        'src/App.tsx': generate_landing_tsx(),
        'src/index.css': """@tailwind base;\n@tailwind components;\n@tailwind utilities;\n\nhtml, body, #root {\n  height: 100%;\n  margin: 0;\n  font-family: system-ui, sans-serif;\n}""",
    }
    
    # Create directories
    (base / 'src').mkdir(parents=True, exist_ok=True)
    
    # Write files
    for file_path, content in files.items():
        full_path = base / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
        print(f"Created: {full_path}")
    
    print(f"\n✅ Project '{project_name}' scaffolded successfully!")
    print(f"\nNext steps:")
    print(f"  1. cd {project_name}")
    print(f"  2. npm install")
    print(f"  3. npm run dev")

def main():
    parser = argparse.ArgumentParser(description="Scaffold 3D web projects")
    parser.add_argument('--type', choices=['r3f', 'vanilla', 'spline'], default='r3f', help='Project type')
    parser.add_argument('--name', default='my-3d-app', help='Project name')
    parser.add_argument('--out', default='.', help='Output directory')
    
    args = parser.parse_args()
    scaffold_project(args.type, args.name, args.out)

if __name__ == '__main__':
    main()