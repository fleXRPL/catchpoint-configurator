# Catchpoint Configurator

A Python-based tool for managing Catchpoint monitoring configurations as code.

## Features

- Deploy and manage Catchpoint tests and dashboards using YAML configurations
- Validate configurations against schemas
- Template support for reusable configurations
- CLI interface for all operations
- Support for both test and dashboard configurations
- Integration with Catchpoint API v2

## Installation

```bash
pip install catchpoint-configurator
```

## Quick Start

1. Set up your Catchpoint API credentials:

```bash
export CATCHPOINT_CLIENT_ID="your_client_id"
export CATCHPOINT_CLIENT_SECRET="your_client_secret"
```

2. Create a test configuration:

```yaml
type: test
name: "my-web-test"
url: "https://example.com"
frequency: 300  # 5 minutes
nodes:
  - "US-East"
  - "US-West"
  - "EU-West"
alerts:
  - name: "High Response Time"
    metric: "response_time"
    threshold: 2000
    operator: ">"
    recipients:
      - email: "alerts@example.com"
```

3. Deploy the configuration:

```bash
catchpoint-configurator deploy test-config.yaml
```

## Usage

### CLI Commands

- `deploy`: Deploy a configuration
- `validate`: Validate a configuration file
- `list`: List existing configurations
- `apply-template`: Apply a template with variables
- `update`: Update an existing configuration
- `delete`: Delete a configuration
- `export`: Export a configuration
- `import-config`: Import a configuration

### Examples

Validate a configuration:
```bash
catchpoint-configurator validate test-config.yaml
```

List all tests:
```bash
catchpoint-configurator list --type test
```

Apply a template:
```bash
catchpoint-configurator apply-template web-test variables.yaml
```

### Configuration Examples

See the `examples/` directory for more configuration examples:
- `test-config.yaml`: Example test configuration
- `dashboard-config.yaml`: Example dashboard configuration
- `templates/web-test.yaml`: Example template
- `templates/variables.yaml`: Example template variables

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/fleXRPL/catchpoint-configurator.git
cd catchpoint-configurator
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Style

```bash
black .
isort .
flake8
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.