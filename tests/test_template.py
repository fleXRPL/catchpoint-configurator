"""Tests for template rendering."""

import pytest
import yaml

from catchpoint_configurator.template import (
    render_template,
    load_template,
    load_variables,
    TemplateError,
)

def test_render_template():
    """Test rendering a template with variables."""
    template = {
        "type": "web",
        "name": "{{ name }}",
        "url": "{{ url }}",
        "frequency": "{{ frequency }}",
        "nodes": "{{ nodes }}",
    }
    variables = {
        "name": "test-web",
        "url": "https://example.com",
        "frequency": 300,
        "nodes": ["US-East", "US-West"],
    }
    result = render_template(template, variables)
    assert result["type"] == "web"
    assert result["name"] == "test-web"
    assert result["url"] == "https://example.com"
    assert result["frequency"] == 300
    assert result["nodes"] == ["US-East", "US-West"]

def test_render_template_missing_variable():
    """Test rendering a template with missing variable."""
    template = {
        "type": "web",
        "name": "{{ name }}",
        "url": "{{ url }}",
    }
    variables = {
        "name": "test-web",
    }
    with pytest.raises(TemplateError) as exc_info:
        render_template(template, variables)
    assert "Missing variable" in str(exc_info.value)

def test_render_template_invalid_syntax():
    """Test rendering a template with invalid syntax."""
    template = {
        "type": "web",
        "name": "{{ name",
        "url": "{{ url }}",
    }
    variables = {
        "name": "test-web",
        "url": "https://example.com",
    }
    with pytest.raises(TemplateError) as exc_info:
        render_template(template, variables)
    assert "Invalid template syntax" in str(exc_info.value)

def test_render_template_with_defaults():
    """Test rendering a template with default values."""
    template = {
        "type": "web",
        "name": "{{ name | default('default-name') }}",
        "url": "{{ url | default('https://default.com') }}",
        "frequency": "{{ frequency | default(300) }}",
    }
    variables = {
        "name": "test-web",
    }
    result = render_template(template, variables)
    assert result["name"] == "test-web"
    assert result["url"] == "https://default.com"
    assert result["frequency"] == 300

def test_render_template_with_conditionals():
    """Test rendering a template with conditional logic."""
    template = {
        "type": "web",
        "name": "{{ name }}",
        "url": "{{ url }}",
        "alerts": [
            {
                "metric": "response_time",
                "threshold": "{{ response_time_threshold | default(3000) }}",
                "enabled": "{{ enable_alerts | default(true) }}",
            }
        ],
    }
    variables = {
        "name": "test-web",
        "url": "https://example.com",
        "response_time_threshold": 5000,
        "enable_alerts": False,
    }
    result = render_template(template, variables)
    assert result["alerts"][0]["threshold"] == 5000
    assert result["alerts"][0]["enabled"] is False

def test_render_template_with_loops():
    """Test rendering a template with loops."""
    template = {
        "type": "web",
        "name": "{{ name }}",
        "url": "{{ url }}",
        "nodes": [
            "{% for node in nodes %}"
            "{{ node }}"
            "{% endfor %}"
        ],
    }
    variables = {
        "name": "test-web",
        "url": "https://example.com",
        "nodes": ["US-East", "US-West", "EU-West"],
    }
    result = renderer.render(template, variables)
    assert result["nodes"] == ["US-East", "US-West", "EU-West"]

def test_render_template_with_filters(renderer):
    """Test rendering a template with filters."""
    template = {
        "type": "web",
        "name": "{{ name | upper }}",
        "url": "{{ url | lower }}",
        "frequency": "{{ frequency | int }}",
    }
    variables = {
        "name": "test-web",
        "url": "HTTPS://EXAMPLE.COM",
        "frequency": "300",
    }
    result = renderer.render(template, variables)
    assert result["name"] == "TEST-WEB"
    assert result["url"] == "https://example.com"
    assert result["frequency"] == 300 