# Eureka Beamline Compose Configuration

This directory contains the podman-compose configuration for the Eureka beamline services.

## Prerequisites

- Podman installed on your system
- Podman Compose installed on your system
- Git installed on your system

## Setup Instructions

1. Build the epics-podman image:
   ```bash
   podman build -t epics-podman:latest https://git.aps.anl.gov/xsd-det/epics-podman.git
   ```

2. Verify your directory structure:
   ```
   eureka_beamline/
   └── compose/
       ├── aps-compose.yml
       └── README.md
   ```

## Recipe

The following commands are used to run the IOCs:

1. Area Detector IOC:
   ```bash
   podman run -it --net=host epics-podman:latest adsim
   ```

2. General Purpose IOC:
   ```bash
   podman run -it --net=host epics-podman:latest gp
   ```

These commands are already configured in the `aps-compose.yml` file under the `command` field for each service.

## Running the Services

You can run the services either using podman-compose or individual podman commands:

### Using podman-compose

1. Navigate to the compose directory:
   ```bash
   cd eureka_beamline/compose
   ```

2. Start the services:
   ```bash
   podman-compose -f aps-compose.yml up
   ```

   To run in detached mode (in the background):
   ```bash
   podman-compose -f aps-compose.yml up -d
   ```

3. To stop the services:
   ```bash
   podman-compose -f aps-compose.yml down
   ```

### Using individual podman commands

1. For the area detector IOC:
   ```bash
   podman run -it --net=host epics-podman:latest adsim
   ```

2. For the general purpose IOC:
   ```bash
   podman run -it --net=host epics-podman:latest gp
   ```

3. For Redis:
   ```bash
   podman run -it docker.io/redis
   ```

## Available Services

- `ioc_adsim`: Simulated area detector IOC (command: `adsim`)
- `ioc_gp_sim`: Simulated general purpose IOC (command: `gp`)
- `redis`: Redis server for message broker

## Volume Mounts

The IOC containers are configured to mount a local directory. You'll need to update the volume paths in `aps-compose.yml` with your desired paths:

```yaml
volumes:
  - /path/to/your/folder:/path/in/container  # Replace with your actual paths
```

## Network Configuration

The IOC containers are configured to use host networking mode (`network_mode: host`), which means they will share the host's network stack.

## Troubleshooting

### Common Container Issues

1. Container fails to start with "failed to exec pid1: No such file or directory":
   ```bash
   # Clean up existing containers and images
   podman-compose -f aps-compose.yml down
   podman system prune -f
   
   # Rebuild the epics-podman image
   podman build -t epics-podman:latest https://git.aps.anl.gov/xsd-det/epics-podman.git
   
   # Start the services
   podman-compose -f aps-compose.yml up
   ```

2. Container attach socket error:
   ```bash
   # Remove the problematic container
   podman rm -f compose_ioc_adsim_1
   
   # Clean up podman's storage
   podman system prune -f
   
   # Restart the service
   podman-compose -f aps-compose.yml up
   ```

3. Permission issues with mounted volumes:
   ```bash
   sudo chown -R $USER:$USER /path/to/your/mounted/folder
   ```

4. To view container logs:
   ```bash
   podman-compose -f aps-compose.yml logs
   ```

### Container Cleanup

If you encounter persistent issues, you can perform a complete cleanup:

```bash
# Stop all containers
podman-compose -f aps-compose.yml down

# Remove all containers, images, and volumes
podman system prune -af --volumes

# Rebuild the epics-podman image
podman build -t epics-podman:latest https://git.aps.anl.gov/xsd-det/epics-podman.git

# Start fresh
podman-compose -f aps-compose.yml up
```

## Additional Resources

- [EPICS Podman Repository](https://git.aps.anl.gov/xsd-det/epics-podman)
- [Podman Documentation](https://docs.podman.io/en/latest/markdown/podman.1.html)
- [Podman Compose Documentation](https://github.com/containers/podman-compose)
