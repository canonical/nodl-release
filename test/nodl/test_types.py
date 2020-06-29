# Copyright 2020 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU Limited General Public License version 3, as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranties of MERCHANTABILITY, SATISFACTORY QUALITY, or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Limited General Public License for more details.
#
# You should have received a copy of the GNU Limited General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.


import nodl.types
import pytest


@pytest.fixture
def topic_publisher():
    return nodl.types.Topic(name='foo', message_type='bar', publisher=True)


def test_action():
    action_server = nodl.types.Action(name='foo', action_type='bar', server=True)
    assert action_server.name == 'foo'
    assert action_server.type == 'bar'
    assert action_server.server


def test_parameter():
    parameter = nodl.types.Parameter(name='foo', parameter_type='bar')
    assert parameter.name == 'foo'
    assert parameter.type == 'bar'


def test_service():
    service_client = nodl.types.Service(name='foo', service_type='bar', client=True)
    assert service_client.name == 'foo'
    assert service_client.type == 'bar'
    assert service_client.client


def test_topic(topic_publisher):
    assert topic_publisher.name == 'foo'
    assert topic_publisher.type == 'bar'
    assert topic_publisher.publisher


def test_representations(topic_publisher):
    assert 'foo' in repr(topic_publisher) and 'bar' in repr(topic_publisher)
    assert 'foo' in str(topic_publisher) and 'bar' in str(topic_publisher)


def test_equality(topic_publisher):
    also_topic_publisher = nodl.types.Topic(name='foo', message_type='bar', publisher=True)
    assert also_topic_publisher == topic_publisher

    not_same_topic_publisher = nodl.types.Topic(name='fiz', message_type='bar', publisher=True,)
    assert not_same_topic_publisher != topic_publisher

    # Test different roles cause inequality
    assert nodl.types.Action(name='foo', action_type='bar', server=True) != nodl.types.Action(
        name='foo', action_type='bar', server=True, client=True
    )


def test_same_name_different_interface_type():
    topic = nodl.types.Topic(name='foo', message_type='bar')
    service = nodl.types.Service(name='foo', service_type='bar')
    assert topic != service


def test_node():
    topic = nodl.types.Topic(name='foo', message_type='bar')
    service = nodl.types.Service(name='baz', service_type='woo')

    node = nodl.types.Node(name='test', executable='toast', topics=[topic], services=[service])
    assert node.name == 'test'
    assert node.executable == 'toast'
    assert node.topics[topic.name] == topic
    assert node.services[service.name] == service
