"""Tests for template rendering."""

from unittest.mock import Mock, patch

import pytest

from catchpoint_configurator.template import TemplateError, render_template


@pytest.fixture
def mock_template_renderer():
    """Create a mock template renderer."""
    return Mock()


def test_render_template(mock_template_renderer):
    """Test rendering a template with variables."""
    with patch("catchpoint_configurator.template.Environment") as mock_env:
        mock_template = Mock()
        mock_template.render.return_value = "rendered template"
        mock_env.return_value.get_template.return_value = mock_template

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
        assert result == "rendered template"
        mock_template.render.assert_called_once_with(**variables)


def test_render_template_missing_variable(mock_template_renderer):
    """Test rendering a template with missing variable."""
    with patch("catchpoint_configurator.template.Environment") as mock_env:
        mock_template = Mock()
        mock_template.render.side_effect = TemplateError("Missing variable")
        mock_env.return_value.get_template.return_value = mock_template

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


def test_render_template_invalid_syntax(mock_template_renderer):
    """Test rendering a template with invalid syntax."""
    with patch("catchpoint_configurator.template.Environment") as mock_env:
        mock_template = Mock()
        mock_template.render.side_effect = TemplateError("Invalid template syntax")
        mock_env.return_value.get_template.return_value = mock_template

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


def test_render_template_with_defaults(mock_template_renderer):
    """Test rendering a template with default values."""
    with patch("catchpoint_configurator.template.Environment") as mock_env:
        mock_template = Mock()
        expected_result = {
            "type": "web",
            "name": "test-web",
            "url": "https://default.com",
            "frequency": 300,
        }
        mock_template.render.return_value = expected_result
        mock_env.return_value.get_template.return_value = mock_template

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
        assert result == expected_result


def test_render_template_with_conditionals(mock_template_renderer):
    """Test rendering a template with conditional logic."""
    with patch("catchpoint_configurator.template.Environment") as mock_env:
        mock_template = Mock()
        expected_result = {
            "type": "web",
            "name": "test-web",
            "url": "https://example.com",
            "alerts": [
                {
                    "metric": "response_time",
                    "threshold": 5000,
                    "enabled": False,
                }
            ],
        }
        mock_template.render.return_value = expected_result
        mock_env.return_value.get_template.return_value = mock_template

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
        assert result == expected_result


def test_render_template_with_loops(mock_template_renderer):
    """Test rendering a template with loops."""
    with patch("catchpoint_configurator.template.Environment") as mock_env:
        mock_template = Mock()
        expected_result = {
            "type": "web",
            "name": "test-web",
            "url": "https://example.com",
            "nodes": ["US-East", "US-West", "EU-West"],
        }
        mock_template.render.return_value = expected_result
        mock_env.return_value.get_template.return_value = mock_template

        template = {
            "type": "web",
            "name": "{{ name }}",
            "url": "{{ url }}",
            "nodes": ["{% for node in nodes %}" "{{ node }}" "{% endfor %}"],
        }
        variables = {
            "name": "test-web",
            "url": "https://example.com",
            "nodes": ["US-East", "US-West", "EU-West"],
        }
        result = render_template(template, variables)
        assert result == expected_result


def test_render_template_with_filters(mock_template_renderer):
    """Test rendering a template with filters."""
    with patch("catchpoint_configurator.template.Environment") as mock_env:
        mock_template = Mock()
        expected_result = {
            "type": "web",
            "name": "TEST-WEB",
            "url": "https://example.com",
            "frequency": 300,
        }
        mock_template.render.return_value = expected_result
        mock_env.return_value.get_template.return_value = mock_template

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
        result = render_template(template, variables)
        assert result == expected_result


def test_render_template_file_not_found():
    """Test rendering a non-existent template file."""
    with pytest.raises(TemplateError, match="Failed to render template nonexistent.yaml"):
        render_template("nonexistent.yaml", {})
