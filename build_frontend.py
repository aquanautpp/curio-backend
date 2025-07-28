#!/usr/bin/env python3
import os
import shutil
import subprocess

def build_and_copy_frontend():
    frontend_path = "../curio-frontend"
    backend_static_path = "src/static"
    vite_api_url = "https://curio-backend-1.onrender.com/api"  # ou pegue de variável de ambiente se preferir

    print("🚀 Fazendo build do frontend...")

    # Instalar dependências
    subprocess.run("pnpm install", shell=True, cwd=frontend_path, check=True)

    # Setar a variável de ambiente no momento do build
    env = os.environ.copy()
    env["VITE_API_BASE_URL"] = vite_api_url

    # Fazer build com variável de ambiente setada
    subprocess.run("pnpm run build", shell=True, cwd=frontend_path, env=env, check=True)

    # Limpar e copiar o build para o backend
    if os.path.exists(backend_static_path):
        shutil.rmtree(backend_static_path)

    frontend_dist = os.path.join(frontend_path, "dist")
    shutil.copytree(frontend_dist, backend_static_path)

    print("✅ Build concluído!")

if __name__ == "__main__":
    build_and_copy_frontend()
