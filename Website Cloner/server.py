import cgi
import http.server
import socketserver
import os
import subprocess
import hashlib
from urllib.parse import parse_qs
from pywebcopy import save_webpage

LOG_FILE = "cloner.log"
README_TEMPLATE = """
# Docker Website Container

This folder contains a Docker image exported as a .tar file, ready to be loaded into Docker Desktop or via CLI.

## Files
- {docker_tar}
- Dockerfile
- nginx.conf (optional, for advanced config)

## How to Use
1. Open Docker Desktop, go to Images, and click 'Load'.
   - Or use CLI: `docker load -i {docker_tar}`
2. The image will appear with the name: {docker_name}
3. To run the container:
   - `docker run -d -p 8080:80 {docker_name}`
   - (Change port as needed)
4. The website will be served by Nginx at http://localhost:8080

## Advanced
- You can edit `nginx.conf` and rebuild the image if needed.
- The Dockerfile is included for reference or customization.

---
MD5 of image: {md5_hash}
"""

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "index.html"
        try:
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        except FileNotFoundError:
            self.send_error(404, "File not found")

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        form = parse_qs(post_data)
        url = form.get("website_url", [""])[0]
        docker_name = form.get("docker_name", [""])[0]
        save_path = form.get("save_path", [""])[0]
        project_folder = os.path.join('./cloned_sites', docker_name)
        log_entries = []

        def log(msg):
            log_entries.append(msg)
            with open(LOG_FILE, "a") as f:
                f.write(msg + "\n")

        if not url or not docker_name or not save_path:
            self.send_error(400, "Bad Request: Missing fields")
            return

        urlN = url if url.startswith("http") else "https://" + url.strip("/")
        if not os.path.isdir(project_folder):
            os.makedirs(project_folder, exist_ok=True)
            try:
                log(f"Cloning {urlN} to {project_folder}")
                save_webpage(
                    url=urlN,
                    project_folder=project_folder,
                    project_name=docker_name
                )
                log("Cloning complete.")
            except Exception as e:
                log(f"Error cloning website: {e}")
                self.send_error(500, f"Error cloning website: {e}")
                return
        # Write Dockerfile for Nginx
        dockerfile_path = os.path.join(project_folder, "Dockerfile")
        with open(dockerfile_path, "w") as f:
            f.write(f"""
FROM nginx:alpine
COPY . /usr/share/nginx/html
EXPOSE 80
CMD [\"nginx\", \"-g\", \"daemon off;\"]
""")
        log("Dockerfile created.")
        # Optionally write nginx.conf for advanced users
        nginx_conf_path = os.path.join(project_folder, "nginx.conf")
        with open(nginx_conf_path, "w") as f:
            f.write("# Default Nginx config. Edit as needed.\n")
        # Build Docker image
        build_cmd = ["docker", "build", "-t", docker_name, project_folder]
        try:
            log(f"Building Docker image: {docker_name}")
            result = subprocess.run(build_cmd, capture_output=True, text=True)
            log(result.stdout)
            log(result.stderr)
            if result.returncode != 0:
                log(f"Docker build failed: {result.stderr}")
                self.send_error(500, f"Docker build failed: {result.stderr}")
                return
            log("Docker build complete.")
        except Exception as e:
            log(f"Error building Docker image: {e}")
            self.send_error(500, f"Error building Docker image: {e}")
            return
        # Get image ID and calculate MD5
        try:
            inspect_cmd = ["docker", "images", "--format", "{{.ID}}", docker_name]
            image_id = subprocess.check_output(inspect_cmd, text=True).strip()
            md5_hash = hashlib.md5(image_id.encode()).hexdigest()
            log(f"Docker image ID: {image_id}")
            log(f"MD5: {md5_hash}")
            # Save image to tar file in chosen location
            docker_tar = os.path.join(save_path, f"{docker_name}.tar")
            save_cmd = ["docker", "save", "-o", docker_tar, docker_name]
            try:
                subprocess.run(save_cmd, check=True)
                log(f"Image saved to: {docker_tar}")
            except Exception as e:
                log(f"Error saving image: {e}")
            # Write README
            readme_path = os.path.join(save_path, f"README_{docker_name}.md")
            with open(readme_path, "w") as f:
                f.write(README_TEMPLATE.format(
                    docker_tar=f"{docker_name}.tar",
                    docker_name=docker_name,
                    md5_hash=md5_hash
                ))
            log(f"README created: {readme_path}")
        except Exception as e:
            log(f"Error getting image ID: {e}")
        # Respond with log and MD5
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(("\n".join(log_entries)).encode())


PORT = 7000
os.makedirs("cloned_sites", exist_ok=True)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with socketserver.TCPServer(("127.0.0.1", PORT), RequestHandler) as s:
    s.allow_reuse_address = True
    print(f"Server running on http://127.0.0.1:{PORT}")
    s.serve_forever()
