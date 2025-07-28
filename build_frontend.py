#!/usr/bin/env python3
import os
import shutil
import subprocess

def build_and_copy_frontend():
    frontend_path = "../curio-frontend"
    backend_static_path = "src/static"
    
    print("🚀 Fazendo build do frontend...")
    
    # Instalar dependências
    subprocess.run("pnpm install", shell=True, cwd=frontend_path, check=True)
    
    # Fazer build
    subprocess.run("pnpm run build", shell=True, cwd=frontend_path, check=True)
    
    # Limpar e copiar
    if os.path.exists(backend_static_path):
        shutil.rmtree(backend_static_path)
    
    frontend_dist = os.path.join(frontend_path, "dist")
    shutil.copytree(frontend_dist, backend_static_path)
    
    print("✅ Build concluído!")

if __name__ == "__main__":
    build_and_copy_frontend()
