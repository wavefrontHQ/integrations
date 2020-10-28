## Overview
SLI runner is a single Go binary that, periodically executes several probes against Concourse, keeping track of the successes and failures. These deployment files are being used by [Concourse CI](https://docs.wavefront.com/concourse.html) integration. Detailed information about SLI runner can be found [here](https://github.com/cirocosta/slirunner).

## Prerequisites
Concourse CI should be up and running.

## Installation
SLI runner can be installed using the below methods:
- Use  **[kubernetes.yaml](https://github.com/wavefrontHQ/integrations/blob/master/concourse/slirunner/kubernetes.yaml)** and replace `CONCOURSE-URL` with the Concourse CI web URL and also pass Concourse CI `Username` and `Password` as data to configure SLI Runner.
- Use **[docker-compose.yml](https://github.com/wavefrontHQ/integrations/blob/master/concourse/slirunner/docker-compose.yml)** and replace below placeholders with their actual values to configure SLI Runner.

    ```
    CONCOURSE-URL       - Concourse Web URL
    CONCOURSE-USERNAME  - Concourse Username
    CONCOURSE-PASSWORD  - Concourse Password
    ```
