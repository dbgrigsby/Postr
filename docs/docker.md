# Installing Docker
  - Linux (Ubuntu 16.04)
      - https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04
  - Mac
      - `brew cask install docker`
      - Press Command + Space to bring up Spotlight Search and enter Docker to launch Docker.
      - In the Docker needs privileged access dialog box, click OK.
      - Enter password and click OK.
      - Wait for Docker to finish loading
  - Windows
      - Not supported well, please use a Linux VM
      - Virtualbox and Vmware are both great for this

# Running Docker
  - Building the image
    - `docker build -t postr .`
  - Running the image
    - `docker run postr`
  - Entering the virtualized environment (mini linux shell)
    - `docker run -it --entrypoint bash postr`
  - Listing all images
    - `docker images`
